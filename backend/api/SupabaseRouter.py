from services.SupabaseAdapters import equipment as supabase_equipment_adapter
from services.SupabaseAdapters import users as supabase_user_adapter
from services.SupabaseAdapters import parks as supabase_parks_adapter
from fastapi import APIRouter
from models.requests.equipment import EquipmentCreate, EquipmentUpdate
from models.requests.users import UserCreate, UserUpdate
from models.requests.parks import ParkCreate, ParkUpdate

router = APIRouter()

# ============================================================
#  Parks
# ============================================================


@router.get("/parks/", tags=["parks"])
async def get_park(id: str | None = None):
    response = await supabase_parks_adapter.get_park(id)
    return response


@router.post("/parks/create", tags=["parks"])
async def create_park(payload: ParkCreate):
    response = await supabase_parks_adapter.create_park(payload)
    return response


@router.put("/parks/update", tags=["parks"])
async def update_park(payload: ParkUpdate):
    response = await supabase_parks_adapter.update_park(payload)
    return response


@router.delete("/parks/delete", tags=["parks"])
async def delete_park(id: str):
    response = await supabase_parks_adapter.delete_park(id)
    return response


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
