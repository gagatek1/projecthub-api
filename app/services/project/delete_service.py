from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.core.database import dynamodb


def delete_service(project_id: str, user):
    table = dynamodb.Table("projects")

    response = table.query(KeyConditionExpression=Key("id").eq(project_id))
    project_owner = response["Items"][0].get("project_owner")

    if project_owner != user.get("Username"):
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        response = table.delete_item(
            Key={
                "id": project_id,
            }
        )
        return response
    except ClientError as e:
        raise HTTPException(detail=e.response["Error"], status_code=500)
