from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def update_service(task, user):
    table = dynamodb.Table("tasks")

    response = table.query(KeyConditionExpression=Key("id").eq(task.id))
    assigned_user = response["Items"][0].get("assigned_user")

    if assigned_user != user.get("Username"):
        raise HTTPException(status_code=403, detail="Forbidden")

    if task.assigned_user is None:
        user_id = user.get("Username")
        task.assigned_user = user_id

    if task.project_id is None:
        project_id = response["Items"][0].get("project_id")
        task.project_id = project_id

    try:
        response = table.update_item(
            Key={
                "id": task.id,
            },
            UpdateExpression=(
                "SET #name = :name, #description = :description, #assigned_user = :assigned_user, #project_id = :project_id"
            ),
            ExpressionAttributeNames={
                "#name": "name",
                "#description": "description",
                "#assigned_user": "assigned_user",
                "#project_id": "project_id",
            },
            ExpressionAttributeValues={
                ":name": task.name,
                ":description": task.description,
                ":assigned_user": task.assigned_user,
                ":project_id": task.project_id,
            },
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes", {})
    except ClientError as e:
        error_message = e.response.get("Error", {}).get("Message", "Unknown error")

        return JSONResponse(content={"error": error_message}, status_code=500)
    except AttributeError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
