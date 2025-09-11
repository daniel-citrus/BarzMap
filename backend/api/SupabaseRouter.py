from services.SupabaseAdapters import equipment_adapter as supabase_equipment_adapter
from services.SupabaseAdapters import user_adapter as supabase_user_adapter
from fastapi import APIRouter
from models.requests.equipment import EquipmentCreate, EquipmentUpdate
from models.requests.users import UserCreate, UserUpdate

router = APIRouter()

#   Park
#       getPark (in radius)?
#       create park (default pending approval)
#       update park (update data, approve or deny)
#       delete park

# ============================================================
#  Parks
# ============================================================

# ============================================================
#  Equipment
# ============================================================


@router.get("/equipment/", tags=["equipment"])
async def get_equipment(id: str | None = None):
    response = await supabase_equipment_adapter.get_equipment(id)
    return response


@router.post("/equipment/create", tags=["equipment"])
async def create_equipment(payload: EquipmentCreate):
    response = await supabase_equipment_adapter.create_equipment(payload)
    return response


@router.put("/equipment/update", tags=["equipment"])
async def update_equipment(payload: EquipmentUpdate):
    response = await supabase_equipment_adapter.update_equipment(payload)
    return response


@router.delete("/equipment/delete", tags=["equipment"])
async def delete_equipment(id: str | None = None):
    response = await supabase_equipment_adapter.delete_equipment(id)
    return response


# ============================================================
#  User
# ============================================================


@router.get("/user/", tags=["users"])
async def get_user(id: str | None = None):
    response = await supabase_user_adapter.get_user(id)
    return response


@router.post("/user/create", tags=["users"])
async def create_user(payload: UserCreate):
    response = await supabase_user_adapter.create_user(payload)
    return response


@router.put("/user/update", tags=["users"])
async def update_user(payload: UserUpdate):
    response = await supabase_user_adapter.update_user(payload)
    return response


@router.delete("/user/delete", tags=["users"])
async def delete_user(id: str):
    response = await supabase_user_adapter.delete_user(id)
    return response
