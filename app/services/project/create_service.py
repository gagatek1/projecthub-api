from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.database import dynamodb


def create_service(project):
    table = dynamodb.Table("projects")

    try:
        project_dict = project.dict()

        table.put_item(Item=project_dict)

        return project
    except ClientError as e:
        return JSONResponse(content=e.response["Error"], status_code=500)
