from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """
    Модель для пользователей.

        id: ID
        email: str
        hashed_password: str
        is_active: bool
        is_superuser: bool
        is_verified: bool
    """
