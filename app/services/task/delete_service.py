from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def delete_service(task_id: str, user):
    table = dynamodb.Table("tasks")

    response = table.query(KeyConditionExpression=Key("id").eq(task_id))
    assigned_user = response["Items"][0].get("assigned_user")

    if assigned_user != user.get("Username"):
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        response = table.delete_item(
            Key={
                "id": task_id,
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
