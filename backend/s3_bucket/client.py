import boto3
from botocore.exceptions import ClientError
from env import LOCAL, LOCALSTACK_ENDPOINT_URL


class S3Interface:
	"""An interface for interacting with S3, handling LocalStack and real environments."""

	def __init__(self):
		self.s3_client = self._create_s3_client()

	def _create_s3_client(self):
		"""Creates an S3 client, configured for LocalStack if running locally."""
		if LOCAL:
			return boto3.client('s3', endpoint_url=LOCALSTACK_ENDPOINT_URL)
		return boto3.client('s3')

	def upload_video(self, bucket_name, file_path, object_key):
		"""Uploads a video to S3.

		Args:
		    bucket_name (str): The name of the S3 bucket.
		    file_path (str): The path to the local video file.
		    object_key (str): The key (name) of the object in S3.

		Raises:
		    ClientError: Any botocore client errors encountered.
		"""
		with open(file_path, 'rb') as f:
			try:
				self.s3_client.upload_fileobj(f, bucket_name, object_key)
			except ClientError as error:
				raise error from None  # Raise the error with proper traceback

	def download_video(self, bucket_name, object_key, destination_path):
		# TODO: fix this
		"""Downloads a video from S3.

		Args:
		    bucket_name (str): The name of the S3 bucket.
		    object_key (str): The key (name) of the object in S3.
		    destination_path (str): The path to save the downloaded video locally.

		Raises:
		    ClientError: Any botocore client errors encountered.
		"""
		try:
			self.s3_client.download_file(bucket_name, object_key, destination_path)
		except ClientError as error:
			raise error from None  # Raise the error with proper traceback

	def list_objects(self, bucket_name) -> dict:
		"""Lists objects in an S3 bucket.

		Args:
		    bucket_name (str): The name of the S3 bucket.

		Returns:
		    dict: The response from the `list_objects` operation.

		Raises:
		    ClientError: Any botocore client errors encountered.
		"""
		try:
			response = self.s3_client.list_objects(Bucket=bucket_name)
			return response
		except ClientError as error:
			raise error from None  # Raise the error with proper traceback
