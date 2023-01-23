import datetime
from pydantic import BaseModel
from typing import Optional


class UserLogin(BaseModel):
    """User Login class"""

    user_id: str
    device_type: str
    masked_ip: str
    masked_device_id: str
    locale: Optional[str]
    app_version: int
    create_date: datetime.date
