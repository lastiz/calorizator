from datetime import datetime

from pydantic import BaseModel


class ProfileSchema(BaseModel):
    """
    Full profile schema
    """
    
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
