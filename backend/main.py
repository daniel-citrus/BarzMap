from fastapi import FastAPI
from api.SupabaseRouter import router as supabase_router

app = FastAPI()
app.include_router(supabase_router, prefix="/db")


# Basic Endpoints
#   Park
#       getPark (in radius)?
#       create park (default pending approval)
#       update park (update data, approve or deny)
#       delete park
#   Equipment
#       get equipment (single or multiple)
#       create equipment
#       update equipment
#       delete equipment
#   Users
#       get user (auth id)
#       create user
#       update user
#       access, name, image, personal information
#       delete user
