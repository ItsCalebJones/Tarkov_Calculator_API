import logging

import requests
from fastapi import APIRouter, BackgroundTasks, Depends

from tarkov_calculator_api.db.dao.tarkov_item_dao import TarkovItemDAO
from tarkov_calculator_api.settings import settings

router = APIRouter()

# Create a logger
logger = logging.getLogger(__name__)


async def refresh_background(tarkov_item_dao: TarkovItemDAO) -> None:
    """
    Refreshes the euro and dollar prices in the background.

    Args:
        tarkov_item_dao (TarkovItemDAO): The data access object for Tarkov items.
    """
    logger.info("Starting to refresh euro and dollar prices.")
    await refresh_euro(tarkov_item_dao)
    await refresh_dollar(tarkov_item_dao)
    logger.info("Refreshed euro and dollar prices.")


async def refresh_euro(tarkov_item_dao: TarkovItemDAO) -> None:
    """
    Refreshes the euro price.

    Args:
        tarkov_item_dao (TarkovItemDAO): The data access object for Tarkov items.
    """
    euro = await tarkov_item_dao.get_tarkov_item_by_id(1)
    euro_response = requests.get(
        f"https://api.tarkov-market.app/api/v1/item?q=euro&x-api-key={settings.tarkov_market_api_key}",
    )
    if euro_response.status_code != requests.status_codes.codes.ok:
        logger.error(
            f"Error with {euro_response.url} {euro_response.status_code} {euro_response.text}",
        )
        return
    euro_data = euro_response.json()[0]

    if euro is None:
        await tarkov_item_dao.create_tarkov_item_model(
            "euro",
            price=euro_data["price"],
            base_price=euro_data["basePrice"],
        )
    else:
        await tarkov_item_dao.update_tarkov_item(
            euro.id,
            price=euro_data["price"],
            base_price=euro_data["basePrice"],
        )


async def refresh_dollar(tarkov_item_dao: TarkovItemDAO) -> None:
    """
    Refreshes the dollar price.

    Args:
        tarkov_item_dao (TarkovItemDAO): The data access object for Tarkov items.
    """
    dollar = await tarkov_item_dao.get_tarkov_item_by_id(2)
    dollar_response = requests.get(
        f"https://api.tarkov-market.app/api/v1/item?q=dollar&x-api-key={settings.tarkov_market_api_key}",
    )
    if dollar_response.status_code != requests.status_codes.codes.ok:
        logger.error(
            f"Error with {dollar_response.url} {dollar_response.status_code} {dollar_response.text}",
        )
        return
    dollar_data = dollar_response.json()[0]

    if dollar is None:
        await tarkov_item_dao.create_tarkov_item_model(
            "dollar",
            price=dollar_data["price"],
            base_price=dollar_data["basePrice"],
        )
    else:
        await tarkov_item_dao.update_tarkov_item(
            dollar.id,
            price=dollar_data["price"],
            base_price=dollar_data["basePrice"],
        )


@router.post("/")
async def send_refresh_request(
    background_task: BackgroundTasks,
    tarkov_item_dao: TarkovItemDAO = Depends(),
) -> None:
    """
    Sends a refresh request to update the euro and dollar prices.

    Args:
        background_task (BackgroundTasks): The background task manager.
        tarkov_item_dao (TarkovItemDAO, optional): The data access object for Tarkov items.

    Returns:
        None
    """
    background_task.add_task(refresh_background, tarkov_item_dao)
