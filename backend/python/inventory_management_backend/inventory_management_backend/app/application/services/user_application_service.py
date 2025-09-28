from app.application.dto.user_dto import UserCreateDTO
from app.adapters.db.base import User
from app.adapters.auth.jwt_manager import JWTManager

# You need to import your SQLAlchemy session from wherever you define it:
from app.adapters.db.session import get_db_session  # Import your function


class UserApplicationService:
    def authenticate_user(self, username: str, password: str):
        if username == "admin" and password == "secret123":
            class User: pass
            user = User()
            user.username = "admin"
            return user
        return None
    
    def register_user(self, user_in: UserCreateDTO):
        # This is an example. Replace this with actual DB logic!
        # Check for duplicate username/email in DB here if you want.
        session = get_db_session()  # Get a new session
        try:
            user = User(
                username=user_in.username,
                email=user_in.email,
                password_hash=JWTManager.get_password_hash(user_in.password)
            )
            session.add(user)
            session.commit()
            session.refresh(user)  # This step assigns user.id from the DB!

            return user
        finally:
            session.close()            