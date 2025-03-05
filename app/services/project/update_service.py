from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.core.database import dynamodb


def update_service(project, user):
    table = dynamodb.Table("projects")

    response = table.query(KeyConditionExpression=Key("id").eq(project.id))
    project_owner = response["Items"][0].get("project_owner")
    if project_owner != user.get("Username"):
        raise HTTPException(detail="Forbidden", status_code=403)

    try:
        response = table.update_item(
            Key={
                "id": project.id,
            },
            UpdateExpression=(
                "SET #name = :name, #description = :description, #max_users = :max_users"
            ),
            ExpressionAttributeNames={
                "#name": "name",
                "#description": "description",
                "#max_users": "max_users",
            },
            ExpressionAttributeValues={
                ":name": project.name,
                ":description": project.description,
                ":max_users": project.max_users,
            },
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes", {})
    except ClientError as e:
        error_message = e.response.get("Error", {}).get("Message", "Unknown error")

        raise HTTPException(detail=error_message, status_code=500)
    except AttributeError as e:
        raise HTTPException(detail=str(e), status_code=400)
