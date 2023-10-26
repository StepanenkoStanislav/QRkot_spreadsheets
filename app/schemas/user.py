from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    Схема для получения информации о пользователе.

        id: models.ID
        email: EmailStr
        is_active: bool = True
        is_superuser: bool = False
        is_verified: bool = False
    """


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания пользователя.

        email: EmailStr
        password: str
        is_active: Optional[bool] = True
        is_superuser: Optional[bool] = False
        is_verified: Optional[bool] = False
    """


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема для изменения пользователя.

        password: Optional[str]
        email: Optional[EmailStr]
        is_active: Optional[bool]
        is_superuser: Optional[bool]
        is_verified: Optional[bool]
    """
