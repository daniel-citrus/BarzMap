from dotenv import load_dotenv
from supabase import create_client
from models.requests.equipment import (
    EquipmentCreate,
    EquipmentUpdate,
    EquipmentDelete,
)
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
    description = payload.description

    response = (
        supabase.table("equipment")
        .update({"name": name, "description": description})
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
