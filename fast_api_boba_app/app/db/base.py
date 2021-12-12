# Import all the models, so that Base has them before being
# imported by Alembic
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

from app.models.business import Business, TopDrink, DrinkReviews # noqa