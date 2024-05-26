from abc import ABC, abstractmethod

from fastapi.responses import JSONResponse


class BaseAppError(Exception, ABC):
    """
    Generic app exception
    """

    status_code: int | None = None
    fields: list[str] = []
    msg: str = "Generic Error"

    def __init__(self, msg: str | None = None, fields: list[str] | None = None) -> None:
        if self.status_code is None:
            raise AttributeError("Must define class attribute status_code")

        if msg is not None:
            self.msg = msg

        if fields is not None:
            self.fields = fields

        super().__init__()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: status_code={self.status_code}, fields={self.fields}, msg={self.msg}"

    def build_response(self) -> JSONResponse:
        """
        Create json response
        """
        content = {
            "error": {
                "status_code": self.status_code,
                "fields": self.fields,
                "message": self.msg,
            },
        }
        return JSONResponse(
            status_code=self.status_code,  # type: ignore
            content=content,
        )
