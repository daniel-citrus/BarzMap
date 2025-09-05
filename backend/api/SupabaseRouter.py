from typing import List, Optional
import services.SupabaseAdapter as supabase_adapter
from fastapi import APIRouter
from models.requests.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
)

router = APIRouter()

#   Park
#       getPark (in radius)?
#       create park (default pending approval)
#       update park (update data, approve or deny)
#       delete park


@router.get("/read/", tags=["equipment"])
async def get_equipment(uuid: str | None = None):
    response = await supabase_adapter.get_equipment(uuid)
    return response


@router.put("/update/", tags=["equipment"])
async def update_equipment(payload: EquipmentUpdate):
    response = await supabase_adapter.update_equipment(payload)
    return response


@router.post("/create", tags=["equipment"])
async def create_equipment(payload: EquipmentCreate):
    response = await supabase_adapter.create_equipment(payload)
    return response


@router.delete("/delete", tags=["equipment"])
async def delete_equipment(uuid: str | None = None):
    reponse = await supabase_adapter.delete_equipment(uuid)
    return reponse


#   Users
#       get user (auth id)
#       create user
#       update user
#       access, name, image, personal information
#       delete user
