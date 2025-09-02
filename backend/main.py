from fastapi import FastAPI
from api.SupabaseAdapter import app as supabase_adapter

app = FastAPI()
app.include_router(supabase_adapter.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}