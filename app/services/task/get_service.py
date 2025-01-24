from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb

table = dynamodb.Table("tasks")


def get_tasks():
    try:
        response = table.scan(AttributesToGet=["id", "name"])
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)


def get_task(id: str):
    try:
        response = table.query(KeyConditionExpression=Key("id").eq(id))
        return response["Items"]
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
