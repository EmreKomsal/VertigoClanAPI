from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ClanCreate(BaseModel):
    name: str
    region: Optional[str] = None

class ClanResponse(BaseModel):
    id: UUID
    name: str
    region: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
