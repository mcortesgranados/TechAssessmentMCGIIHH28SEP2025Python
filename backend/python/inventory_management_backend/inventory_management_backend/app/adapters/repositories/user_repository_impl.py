from app.adapters.db.session import get_db_session
from app.adapters.db.base import User

class UserRepositoryImpl:
    """
    Infrastructure Service (Adapter):
    Implements user repository interface.
    Handles all DB access using SQLAlchemy.
    """
    def __init__(self, session=None):
        self.session = session or get_db_session()

    def get_user_by_username(self, username):
        return self.session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def create_user(self, username, hashed_password, email):
        user = User(username=username, password_hash=hashed_password, email=email)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user