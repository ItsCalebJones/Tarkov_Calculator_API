import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_docs_router_html(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests the docs router."""
    url = fastapi_app.url_path_for("swagger_ui_html")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"


@pytest.mark.anyio
async def test_docs_router(
    fastapi_app: FastAPI,
    client: AsyncClient,
) -> None:
    """Tests the docs router."""
    url = fastapi_app.url_path_for("swagger_ui_html")
    response = await client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "text/html; charset=utf-8"
