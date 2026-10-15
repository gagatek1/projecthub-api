from datetime import UTC, datetime
from typing import Annotated

from pynamodb.attributes import NumberAttribute, UnicodeAttribute, UTCDateTimeAttribute

from app.shared.entities.base import BaseEntity


class ProjectEntity(BaseEntity, discriminator="project"):
    id: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    name: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    description: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    max_users: Annotated[NumberAttribute, int] = NumberAttribute()
    project_owner: Annotated[UnicodeAttribute, str] = UnicodeAttribute()
    created_at: Annotated[UTCDateTimeAttribute, datetime] = UTCDateTimeAttribute(default=lambda: datetime.now(UTC))

    @property
    def _pk(self) -> str:
        return "project"

    @property
    def _sk(self) -> str:
        return f"project#{self.id}"
