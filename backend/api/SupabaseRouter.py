from typing import List, Optional
import services.SupabaseAdapter as supabase_adapter
from fastapi import APIRouter
from models.requests.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentDelete,
)

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


@router.put("/update/", tags=["update"])
async def update_equipment(payload: EquipmentUpdate):
    response = await supabase_adapter.update_equipment(payload)
    return response


#       add equipment
#       delete equipment

#   Users
#       get user (auth id)
#       create user
#       update user
#       access, name, image, personal information
#       delete user
