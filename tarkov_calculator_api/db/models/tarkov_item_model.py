from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Integer, String

from tarkov_calculator_api.db.base import Base


class TarkovItem(Base):
    """Model for demo purpose."""

    __tablename__ = "tarkov_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=200))  # noqa: WPS432
    price: Mapped[int] = mapped_column(Integer())  # noqa: WPS432
    base_price: Mapped[int] = mapped_column(Integer())  # noqa: WPS432
