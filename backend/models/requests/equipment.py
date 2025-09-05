from pydantic import BaseModel


class EquipmentCreate(BaseModel):
    name: str
    description: str
    icon_name: str


class EquipmentUpdate(BaseModel):
    id: str
    name: str
    description: str | None = None
