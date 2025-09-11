from dotenv import load_dotenv
from supabase import create_client
from models.requests.equipment import EquipmentCreate, EquipmentUpdate
from models.requests.users import UserCreate, UserUpdate
import uuid
import os

load_dotenv(".env.backend")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)


async def get_equipment(id: str | None = None):
    id = uuid.UUID(id)
    response = supabase.table("equipment").select("*").eq("id", str(id)).execute()
    return response.data


async def update_equipment(payload: EquipmentUpdate):
    id = payload.id
    name = payload.name
    icon_name = payload.icon_name
    description = payload.description

    response = (
        supabase.table("equipment")
        .update({"name": name, "description": description, "icon_name": icon_name})
        .eq("id", str(id))
        .execute()
    )

    return response.data


async def create_equipment(payload: EquipmentCreate):
    name = payload.name
    description = payload.description
    icon_name = payload.icon_name

    response = (
        supabase.table("equipment")
        .insert({"name": name, "description": description, "icon_name": icon_name})
        .execute()
    )

    return response.data


async def delete_equipment(id: str | None = None):
    id = uuid.UUID(id)

    response = supabase.table("equipment").delete().eq("id", id).execute()

    return response.data


async def create_user(payload: UserCreate):
    auth0 = payload.auth0_id
    email = payload.email
    name = payload.name
    role = payload.role

    response = (
        supabase.table("users")
        .insert({"auth0_id": auth0, "email": email, "name": name, "role": role})
        .execute()
    )

    return response.data


async def get_user(uuid: str | None = None):
    id = uuid.UUID(uuid)
    response = supabase.table("users").select("*").eq("id", str(id)).execute()
    return response.data
