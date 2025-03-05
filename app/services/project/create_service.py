from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def create_service(project, user):
    table = dynamodb.Table("projects")

    try:
        project_dict = project.dict()

        user_id = user.get("Username")

        project_dict["project_owner"] = user_id

        table.put_item(Item=project_dict)

        return project_dict
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
