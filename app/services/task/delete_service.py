from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def delete_service(task_id: str):
    table = dynamodb.Table("tasks")

    try:
        response = table.delete_item(
            Key={
                "id": task_id,
            }
        )
        return response
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
