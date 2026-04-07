from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from scalar_fastapi import get_scalar_api_reference
from src.domain.exceptions import DomainError
from src.api.v1 import auth_router, me_router

app = FastAPI(title="Marketplace API",
    description="""
    ## REST API для управления маркетплейсом.

    ### Основной функционал:
    * **Auth**: Авторизация через OAuth2 (JWT Bearer)
    * **Products**: Управление каталогом товаров и категориями
    * **UOW**: Асинхронное управление транзакциями

    ---
    *Developer: Yuuki*
    """,
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url=None)

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.__class__.__name__,
            "message": exc.message
        }
    )

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        dark_mode=True, 
    )

app.include_router(auth_router)
app.include_router(me_router)