from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tarkov_calculator_api.db.dao.tarkov_item_dao import TarkovItemDAO
from tarkov_calculator_api.settings import settings
from tarkov_calculator_api.web.api.refresh.views import refresh_dollar, refresh_euro


@pytest.mark.anyio
async def test_refresh_request(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests the endpoint for sending a refresh request.

    This test function sends a POST request to the refresh endpoint and asserts that the response
    status code is 200 (OK). It also asserts that the `BackgroundTasks.add_task` method is called
    once.

    Args:
        fastapi_app (FastAPI): The FastAPI application instance.
        client (AsyncClient): The HTTP client for making requests.

    Returns:
        None
    """
    url = fastapi_app.url_path_for("send_refresh_request")

    with patch("fastapi.BackgroundTasks.add_task") as mock:
        response = await client.post(url)
        assert response.status_code == status.HTTP_200_OK
        mock.assert_called_once()


@pytest.mark.anyio
async def test_handle_refresh(dbsession: AsyncSession) -> None:
    """Tests the handling of refresh requests.

    This test function creates two TarkovItem models in the database, one for "euro" and one for "dollar".
    It then mocks the response from the Tarkov Market API and calls the `refresh_euro` and `refresh_dollar`
    functions to update the prices of the items in the database. Finally, it asserts that the prices of the
    items have been updated correctly.

    Args:
        dbsession (AsyncSession): The async database session.

    Returns:
        None
    """
    dao = TarkovItemDAO(dbsession)

    await dao.create_tarkov_item_model("euro", 25, 50)
    euro = await dao.get_tarkov_item_by_id(1)
    assert euro is not None
    assert euro.price == 25
    assert euro.base_price == 50

    await dao.create_tarkov_item_model("dollar", 75, 100)
    dollar = await dao.get_tarkov_item_by_id(2)
    assert dollar is not None
    assert dollar.price == 75
    assert dollar.base_price == 100

    # Mock the response from the Tarkov Market API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "name": "Euro",
            "price": 100,
            "basePrice": 50,
        },
    ]

    with patch("requests.get", return_value=mock_response) as mock_get_dollar:
        # Call the refresh_euro function
        await refresh_euro(dao)
        # Assert that the requests.get method is called with the correct URL
        mock_get_dollar.assert_called_once_with(
            f"https://api.tarkov-market.app/api/v1/item?q={euro.name}&x-api-key={settings.tarkov_market_api_key}",
        )

    item = await dao.get_tarkov_item_by_id(1)
    assert item is not None
    assert item.price == 100
    assert item.base_price == 50

    # Mock the response from the Tarkov Market API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "name": "Euro",
            "price": 100,
            "basePrice": 50,
        },
    ]

    with patch("requests.get", return_value=mock_response) as mock_get_euro:
        # Call the refresh_euro function
        await refresh_dollar(dao)
        # Assert that the requests.get method is called with the correct URL
        mock_get_euro.assert_called_once_with(
            f"https://api.tarkov-market.app/api/v1/item?q={dollar.name}&x-api-key={settings.tarkov_market_api_key}",
        )

    item = await dao.get_tarkov_item_by_id(2)
    assert item is not None
    assert item.price == 100
    assert item.base_price == 50
