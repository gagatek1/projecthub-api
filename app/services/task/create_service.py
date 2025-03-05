from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def create_service(task, user):
    table = dynamodb.Table("tasks")

    try:
        task_dict = task.dict()

        if task_dict.get("assigned_user") is None:
            user_id = user.get("Username")
            task_dict["assigned_user"] = user_id

        table.put_item(Item=task_dict)

        return task_dict
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
