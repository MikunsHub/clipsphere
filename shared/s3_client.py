from typing import NamedTuple, Optional

import boto3
from botocore.exceptions import ClientError


class S3Config(NamedTuple):
	localstack_endpoint_url: Optional[str]
	local: Optional[str]

class S3Interface:
	def __init__(self, config:S3Config):
		self.local = config.local
		self.localstack_endpoint_url = config.localstack_endpoint_url
		self.s3_client = self._create_s3_client()

	def _create_s3_client(self):
		if self.local:
			return boto3.client('s3', endpoint_url=self.localstack_endpoint_url)
		return boto3.client('s3')

	def generate_presigned_url(self, bucket_name, object_key, expiration):
		try:
			url = self.s3_client.generate_presigned_url(
				'get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=expiration
			)
			return url
		except ClientError as error:
			raise error from None

	def _initiate_multipart_upload(self, bucket_name, object_key):
		response = self.s3_client.create_multipart_upload(Bucket=bucket_name, Key=object_key)
		return response['UploadId']

	def _upload_parts(self, bucket_name, file_obj, upload_id, object_key):
		try:
			part_number = 1
			uploaded_parts = []

			while True:
				# Read a part of the file
				part_data = file_obj.read(10000000)
				if not part_data:
					break

				# Upload the part
				response = self.s3_client.upload_part(
					Bucket=bucket_name,
					Key=object_key,
					PartNumber=part_number,
					UploadId=upload_id,
					Body=part_data,
				)
				# Keep track of the uploaded part
				uploaded_part = {'PartNumber': part_number, 'ETag': response['ETag']}
				uploaded_parts.append(uploaded_part)

				# Increment part number for the next part
				part_number += 1

				# Reset part_number to 1 if it exceeds 10000
				if part_number > 10000:
					part_number = 1

			return uploaded_parts

		except ClientError as error:
			# Handle errors
			raise error from None

	def _complete_multipart_upload(self, bucket_name, upload_id, object_key, uploaded_parts):
		try:
			self.s3_client.complete_multipart_upload(
				Bucket=bucket_name, Key=object_key, UploadId=upload_id, MultipartUpload={'Parts': uploaded_parts}
			)
		except ClientError as error:
			self.s3_client.abort_multipart_upload(Bucket=bucket_name, Key=object_key, UploadId=upload_id)
			raise error from None

	def small_file_upload(self, bucket_name, file_obj, object_key):
		try:
			self.s3_client.upload_fileobj(file_obj, bucket_name, object_key)
		except ClientError as error:
			raise error from None

	def large_file_upload(self, bucket_name, file_obj, object_key):
		try:
			upload_id = self._initiate_multipart_upload(bucket_name, object_key)
			uploaded_parts = self._upload_parts(bucket_name, file_obj, upload_id, object_key)
			self._complete_multipart_upload(bucket_name, upload_id, object_key, uploaded_parts)
		except ClientError as error:
			raise error from None
			raise error from None
