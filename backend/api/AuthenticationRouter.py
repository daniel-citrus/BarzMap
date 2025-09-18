from fastapi import APIRouter
from services.Authentication import authentication

router = APIRouter()


@router.get("/validate/", tags=["Authentication"])
def valid_user() -> bool:
    response = authentication.validate_user()
    return response
