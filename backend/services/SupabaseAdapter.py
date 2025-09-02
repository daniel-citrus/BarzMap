from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv('.env.backend')
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

async def get_equipment():
    response = supabase.table("equipment").select("*").execute()
    return response.data