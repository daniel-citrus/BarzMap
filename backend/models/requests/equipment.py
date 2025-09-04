from pydantic import BaseModel
from typing import List
import uuid


class EquipmentCreate(BaseModel):
    name: str
    description: str
    icon_name: str


class EquipmentUpdate(BaseModel):
    id: str
    name: str
    description: str | None = None


class EquipmentDelete(BaseModel):
    ids: List[uuid.UUID]
