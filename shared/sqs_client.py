import boto3

LOCAL = 1
LOCALSTACK_ENDPOINT_URL='http://localhost:4566'

class S3Interface:
	def __init__(self):
		self.s3_client = self._create_s3_client()

	def _create_s3_client(self):
		if LOCAL:
			return boto3.client('s3', endpoint_url=LOCALSTACK_ENDPOINT_URL)
		return boto3.client('s3')

