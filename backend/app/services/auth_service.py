from fastapi import HTTPException, status
from app.schemas.auth_schema import Register, Login
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.utils.security import (
    hash_password, verify_password,
    create_access_token,
)
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    @staticmethod
    async def register_user(user_data: Register, db: AsyncSession) -> str:
        repo = UserRepository(db)

        existing_user = await repo.get_by_email(str(user_data.email))
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким номером уже существует"
            )

        new_user = User(
            email=str(user_data.email),
            hashed_password=hash_password(user_data.password),
            full_name=user_data.full_name
        )

        created_user = await repo.create(new_user)
        return create_access_token(data={"sub": created_user.email})

    @staticmethod
    async def login_user(user_data: Login, db: AsyncSession) -> str:
        repo = UserRepository(db)
        user = await repo.get_by_email(user_data.email)

        if not user or not verify_password(
                user_data.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный номер телефона или пароль"
            )

        return create_access_token(data={"sub": user.email})

    @staticmethod
    async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
        repo = UserRepository(db)
        return await repo.get_by_email(email)
