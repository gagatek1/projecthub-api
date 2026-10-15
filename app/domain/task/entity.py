from datetime import UTC, datetime
from typing import Annotated
from uuid import uuid4

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

from app.shared.entities.base import BaseEntity


class TaskEntity(BaseEntity, discriminator="task"):
    id: Annotated[UnicodeAttribute, str] = UnicodeAttribute(default=lambda: str(uuid4()))
    name: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    description: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    project_id: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    assigned_user: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    created_at: Annotated[UTCDateTimeAttribute, datetime] = UTCDateTimeAttribute(default=lambda: datetime.now(UTC))

    @property
    def _pk(self) -> str:
        return f"project#{self.project_id}"

    @property
    def _sk(self) -> str:
        return f"task#{self.id}"
