from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from supabase import create_client
import os
import services.SupabaseAdapter as supabase_adapter

app = FastAPI()
router = APIRouter()

@router.get("/equipment/", tags=["equipment"])
async def get_equipment():
    response = supabase_adapter.get_equipment()
    return response.data

app.include_router(router)