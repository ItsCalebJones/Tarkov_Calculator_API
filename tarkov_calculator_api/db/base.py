from sqlalchemy.orm import DeclarativeBase

from tarkov_calculator_api.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
