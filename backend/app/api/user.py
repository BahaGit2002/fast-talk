from fastapi import APIRouter, Depends
from app.models import User
from app.schemas.user_schema import UserResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
