from typing import NamedTuple, Optional

import boto3
from botocore.exceptions import ClientError


class Config(NamedTuple):
	localstack_endpoint_url: Optional[str]
	local: Optional[str]

class SQS_Interface:
	def __init__(self,config:Config):
		self.s3_client = self._create_sqs_client()
		self.local = config.local
		self.localstack_endpoint_url = config.localstack_endpoint_url

	def _create_sqs_client(self):
		if self.local:
			return boto3.client('sqs', endpoint_url=self.localstack_endpoint_url)
		return boto3.client('sqs')

