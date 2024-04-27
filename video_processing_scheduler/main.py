from aws_lambda_typing.context import Context
from aws_lambda_typing.events import S3Event
from shared.sqs_client import S3Interface

def transcode_task_dispatcher(event: S3Event, _context: Context) -> None:
    try:
        object_key = event['Records'][0]['s3']['object']['key']
    except Exception as e:
        raise e


def test_shared():
    s3client = S3Interface()

