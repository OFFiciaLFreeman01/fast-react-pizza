from fastapi import APIRouter, HTTPException

from app.config import settings
from app.schemas.auth import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    valid_user = body.username == settings.admin_username
    valid_password = bool(settings.admin_password_hash) and verify_password(
        body.password, settings.admin_password_hash
    )
    if not (valid_user and valid_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(subject=body.username))
