from fastapi.routing import APIRouter

from tarkov_calculator_api.web.api import docs, monitoring, refresh, tarkov_item

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(
    tarkov_item.router,
    prefix="/tarkov_item",
    tags=["tarkov_item"],
)
api_router.include_router(refresh.router, prefix="/refresh", tags=["refresh"])
