from fastapi import status, Request
from fastapi.responses import JSONResponse

from app.core.base import BaseAppError


async def app_error_handler(request: Request, exc: BaseAppError) -> JSONResponse:
    """
    Handler for overall app errors
    """
    return exc.build_response()
