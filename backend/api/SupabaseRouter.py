from typing import List, Optional
import services.SupabaseAdapter as supabase_adapter
from fastapi import APIRouter
from models.requests.equipment import EquipmentCreate, EquipmentUpdate
from models.requests.users import UserCreate, UserUpdate

router = APIRouter()

#   Park
#       getPark (in radius)?
#       create park (default pending approval)
#       update park (update data, approve or deny)
#       delete park


@router.get("/equipment/", tags=["equipment"])
async def get_equipment(uuid: str | None = None):
    response = await supabase_adapter.get_equipment(uuid)
    return response


@router.put("/equipment/update", tags=["equipment"])
async def update_equipment(payload: EquipmentUpdate):
    response = await supabase_adapter.update_equipment(payload)
    return response


@router.post("/equipment/create", tags=["equipment"])
async def create_equipment(payload: EquipmentCreate):
    response = await supabase_adapter.create_equipment(payload)
    return response


@router.delete("/equipment/delete", tags=["equipment"])
async def delete_equipment(uuid: str | None = None):
    reponse = await supabase_adapter.delete_equipment(uuid)
    return reponse


#   Users
#       get user (auth id)
#       create user
#       update user
#       access, name, image, personal information
#       delete user
@router.get("/user/", tags=["users"])
async def get_user(uuid: str | None = None):
    response = await supabase_adapter.get_user(uuid)
    return response


@router.post("/user/create", tags=["users"])
async def create_user(payload: UserCreate):
    response = await supabase_adapter.create_user(payload)
    return response
