from fastapi import FastAPI
from api.SupabaseRouter import router as supabase_router

app = FastAPI()
app.include_router(supabase_router, prefix="")