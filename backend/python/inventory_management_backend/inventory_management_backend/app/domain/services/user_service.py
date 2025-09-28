from app.adapters.repositories.user_repository_impl import UserRepositoryImpl
from app.adapters.auth.jwt_manager import JWTManager
from app.application.dto.user_dto import UserCreateDTO
from app.adapters.db.base import User

class UserService:
    """
    Domain Service:
    Pure business logic for user registration.
    Does not depend on HTTP, frameworks, or direct DB code.
    """
    def __init__(self, user_repository: UserRepositoryImpl):
        self.user_repository = user_repository

    def register_user(self, user_in: UserCreateDTO) -> User:
        if self.user_repository.get_user_by_username(user_in.username):
            raise ValueError("Username already registered")
        if self.user_repository.get_user_by_email(user_in.email):
            raise ValueError("Email already registered")
        hashed_pw = JWTManager.get_password_hash(user_in.password)
        user = self.user_repository.create_user(
            username=user_in.username,
            hashed_password=hashed_pw,
            email=user_in.email
        )
        return user