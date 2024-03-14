from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tarkov_calculator_api.db.dependencies import get_db_session
from tarkov_calculator_api.db.models.tarkov_item_model import TarkovItem


class TarkovItemDAO:
    """Class for accessing TarkovItem table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_tarkov_item_model(
        self,
        name: str,
        price: int,
        base_price: int,
    ) -> None:
        """
        Add single TarkovItem to session.

        :param name: name of a tarkov item.
        :param price: price of a tarkov item.
        :param base_price: base price of a tarkov item.
        """
        self.session.add(TarkovItem(name=name, price=price, base_price=base_price))

    async def get_all_tarkov_items(self, limit: int, offset: int) -> List[TarkovItem]:
        """
        Get all tarkov item models with limit/offset pagination.

        :param limit: limit of tarkov items.
        :param offset: offset of tarkov items.
        :return: stream of tarkov items.
        """
        raw_tarkov_items = await self.session.execute(
            select(TarkovItem).limit(limit).offset(offset),
        )

        return list(raw_tarkov_items.scalars().fetchall())

    async def filter(
        self,
        name: Optional[str] = None,
    ) -> List[TarkovItem]:
        """
        Get specific tarkov item model.

        :param name: name of tarkov item instance.
        :return: tarkov item models.
        """
        query = select(TarkovItem)
        if name:
            query = query.where(TarkovItem.name == name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())

    async def update_tarkov_item(
        self,
        item_id: int,
        name: Optional[str] = None,
        price: Optional[int] = None,
        base_price: Optional[int] = None,
    ) -> None:
        """
        Update a TarkovItem by its ID.

        :param item_id: ID of the TarkovItem to update.
        :param name: New name of the TarkovItem.
        :param price: New price of the TarkovItem.
        :param base_price: New base_price of the TarkovItem.
        :raises ValueError: TarkovItem with ID not found
        """
        query = select(TarkovItem).where(TarkovItem.id == item_id)
        result = await self.session.execute(query)
        item = result.scalar_one_or_none()

        if item is None:
            raise ValueError(f"TarkovItem with ID {item_id} not found")

        if name is not None:
            item.name = name
        if price is not None:
            item.price = price
        if base_price is not None:
            item.base_price = base_price

        self.session.add(item)
        await self.session.commit()

    async def get_tarkov_item_by_id(self, item_id: int) -> Optional[TarkovItem]:
        """
        Get a TarkovItem by its ID.

        :param item_id: ID of the TarkovItem.
        :return: TarkovItem if found, None otherwise.
        """
        query = select(TarkovItem).filter(TarkovItem.id == item_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
