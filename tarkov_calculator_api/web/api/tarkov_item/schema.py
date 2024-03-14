from pydantic import BaseModel


class TarkovItemModelDTO(BaseModel):
    """
    DTO for TarkovItem models.

    It returned when accessing TarkovItem models from the API.
    """

    id: int
    name: str
    price: int
    base_price: int

    class Config:
        orm_mode = True


class TarkovItemModelInputDTO(BaseModel):
    """DTO for creating new TarkovItem model."""

    name: str
    price: int
    base_price: int
