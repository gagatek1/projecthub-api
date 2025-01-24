from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def create_service(task):
    table = dynamodb.Table("tasks")

    try:
        task_dict = task.dict()

        table.put_item(Item=task_dict)

        return task
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
