import random
import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tarkov_calculator_api.db.dao.tarkov_item_dao import TarkovItemDAO


@pytest.mark.anyio
async def test_getting_list(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests tarkov item instance retrieval."""
    dao = TarkovItemDAO(dbsession)

    created_items = []

    for _ in range(5):
        test_name = uuid.uuid4().hex
        price = random.randint(1, 1000)
        base_price = random.randint(1, 1000)
        await dao.create_tarkov_item_model(
            name=test_name,
            price=price,
            base_price=base_price,
        )
        created_items.append(
            {
                "name": test_name,
                "price": price,
                "base_price": base_price,
            },
        )

    url = fastapi_app.url_path_for("get_tarkov_item_models")
    response = await client.get(url)
    tarkov_items = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(tarkov_items) == len(created_items)

    for item in tarkov_items:
        assert any(
            item["name"] == created_item["name"]
            and item["price"] == created_item["price"]
            and item["base_price"] == created_item["base_price"]
            for created_item in created_items
        )


@pytest.mark.anyio
async def test_getting_by_id(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
) -> None:
    """Tests tarkov item instance retrieval by id."""
    dao = TarkovItemDAO(dbsession)

    test_name = uuid.uuid4().hex
    price = random.randint(1, 1000)
    base_price = random.randint(1, 1000)
    await dao.create_tarkov_item_model(
        name=test_name,
        price=price,
        base_price=base_price,
    )

    item_list = await dao.filter(name=test_name)
    created_item = item_list[0]
    assert created_item.name == test_name
    assert created_item.price == price
    assert created_item.base_price == base_price

    url = fastapi_app.url_path_for(
        "get_tarkov_item_model_by_id",
        tarkov_item_id=created_item.id,
    )
    response = await client.get(url)
    tarkov_item = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert tarkov_item["name"] == created_item.name
    assert tarkov_item["price"] == created_item.price
    assert tarkov_item["base_price"] == created_item.base_price
