from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def update_service(project):
    table = dynamodb.Table("projects")

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

        return JSONResponse(content={"error": error_message}, status_code=500)
    except AttributeError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
