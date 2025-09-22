import jwt
from fastapi import HTTPException, Header, Depends


def get_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    return authorization.split(" ", 1)[1]


def validate_token(token = Depends(get_token)):
    return jwt.decode(token)


def validate_user(token=Depends(validate_token)) -> bool:
    return token
