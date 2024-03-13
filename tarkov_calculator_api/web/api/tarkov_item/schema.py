from pydantic import BaseModel, ConfigDict


class TarkovItemModelDTO(BaseModel):
    """
    DTO for TarkovItem models.

    It returned when accessing TarkovItem models from the API.
    """

    id: int
    name: str
    price: int
    base_price: int
    model_config = ConfigDict(from_attributes=True)


class TarkovItemModelInputDTO(BaseModel):
    """DTO for creating new TarkovItem model."""

    name: str
    price: int
    base_price: int
