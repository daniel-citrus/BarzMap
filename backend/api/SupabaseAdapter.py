from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from supabase import create_client, Client
import os

load_dotenv('.env.backend')
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")

app = FastAPI()
router = APIRouter()
supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

@router.get("/equipment/", tags=["equipment"])
async def get_equipment():
    response = supabase.table("equipment").select("*").execute()
    return response.data

app.include_router(router)