from typing import Annotated, Any

from pynamodb.attributes import DiscriminatorAttribute, UnicodeAttribute
from pynamodb.connection import Connection
from pynamodb.models import Model
from pynamodb.transactions import TransactWrite

from app.settings import dynamodb_settings


class BaseEntity(Model):
    class Meta:  # ty: ignore[invalid-attribute-override]
        table_name = dynamodb_settings.table
        region = dynamodb_settings.region
        host = dynamodb_settings.host or None
        billing_mode = "PAY_PER_REQUEST"
        connect_timeout_seconds = 2
        read_timeout_seconds = 5
        max_retry_attempts = 3

    pk: Annotated[UnicodeAttribute, str] = UnicodeAttribute(hash_key=True)
    sk: Annotated[UnicodeAttribute, str] = UnicodeAttribute(range_key=True)
    type: Annotated[DiscriminatorAttribute, str] = DiscriminatorAttribute()

    def __init__(
        self,
        hash_key: Any = None,
        range_key: Any = None,
        _user_instantiated: bool = True,
        **attributes: Any,
    ) -> None:
        super().__init__(hash_key, range_key, _user_instantiated, **attributes)
        if _user_instantiated:
            self._sync_keys()

    def save(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        self._sync_keys()
        return super().save(*args, **kwargs)

    def _sync_keys(self) -> None:
        self.pk = self._pk
        self.sk = self._sk

    @property
    def _pk(self) -> str:
        raise NotImplementedError

    @property
    def _sk(self) -> str:
        raise NotImplementedError


def transaction() -> TransactWrite:
    connection = Connection(
        region=dynamodb_settings.region,
        host=dynamodb_settings.host or None,
        connect_timeout_seconds=2,
        read_timeout_seconds=5,
        max_retry_attempts=3,
    )
    return TransactWrite(connection=connection)
