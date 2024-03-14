from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends

from tarkov_calculator_api.db.dao.tarkov_item_dao import TarkovItemDAO
from tarkov_calculator_api.db.models.tarkov_item_model import TarkovItem
from tarkov_calculator_api.web.api.tarkov_item.schema import TarkovItemModelDTO

router = APIRouter()


@router.get("/", response_model=List[TarkovItemModelDTO])
async def get_tarkov_item_models(
    limit: int = 10,
    offset: int = 0,
    tarkov_item_dao: TarkovItemDAO = Depends(),
) -> List[TarkovItem]:
    """
    Retrieve all tarkov_item objects from the database.

    :param limit: limit of tarkov_item objects, defaults to 10.
    :param offset: offset of tarkov_item objects, defaults to 0.
    :param tarkov_item_dao: DAO for tarkov_item models.
    :return: list of tarkov_item objects from database.
    """
    return await tarkov_item_dao.get_all_tarkov_items(limit=limit, offset=offset)


@router.get("/{tarkov_item_id}", response_model=TarkovItemModelDTO)
async def get_tarkov_item_model_by_id(
    tarkov_item_id: int,
    tarkov_item_dao: TarkovItemDAO = Depends(),
) -> TarkovItem:
    """
    Retrieve a single tarkov_item object from the database.

    :param tarkov_item_id: id of tarkov_item object.
    :param tarkov_item_dao: DAO for tarkov_item models.
    :return: tarkov_item object from database.
    :raises HTTPException: If the tarkov_item is not found in the database.
    """
    tarkov_item = await tarkov_item_dao.get_tarkov_item_by_id(tarkov_item_id)
    status_code_not_found = 404
    if tarkov_item is None:
        raise HTTPException(
            status_code=status_code_not_found,
            detail="Tarkov item not found",
        )
    return tarkov_item
