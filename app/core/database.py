from os import getenv

from boto3 import resource

dynamodb = resource(
    "dynamodb",
    aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=getenv("REGION_NAME"),
)

tables = [
    {
        "TableName": "projects",
        "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
    },
]


def create_tables():
    try:
        for table in tables:
            dynamodb.create_table(
                TableName=table["TableName"],
                KeySchema=table["KeySchema"],
                AttributeDefinitions=table["AttributeDefinitions"],
            )
    except Exception as e:
        print(e)
