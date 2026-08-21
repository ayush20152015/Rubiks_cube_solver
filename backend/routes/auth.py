import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field

from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()
auth_service = AuthService()


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(credentials: Credentials) -> dict[str, bool]:
    try:
        auth_service.register(credentials.email, credentials.password)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return {"success": True}


@router.post("/login")
def login(credentials: Credentials) -> dict[str, str]:
    token = auth_service.authenticate(credentials.email, credentials.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, str]:
    try:
        return auth_service.user_from_token(credentials.credentials)
    except jwt.InvalidTokenError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from error