from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.domain.exceptions import DomainError
from src.api.v1 import auth_router

app = FastAPI()

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

app.include_router(auth_router)