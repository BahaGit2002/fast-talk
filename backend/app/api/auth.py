from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas.auth_schema import Register, Login, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=Token, status_code=status.HTTP_201_CREATED
)
async def register(user_data: Register, db: AsyncSession = Depends(get_db)):
    access_token = await AuthService.register_user(user_data, db)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(user_data: Login, db: AsyncSession = Depends(get_db)):
    access_token = await AuthService.login_user(user_data, db)
    return {"access_token": access_token, "token_type": "bearer"}
