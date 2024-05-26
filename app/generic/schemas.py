from pydantic import BaseModel


class GenericResponse(BaseModel):
    """
    Generic response scheme
    """

    status_code: int
    msg: str
