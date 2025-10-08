from app.adapters.db.session import get_db_session
from app.adapters.db.base import User

class UserRepositoryImpl:
    """
    Infrastructure Service (Adapter) for User entity.

    Implements methods for accessing and manipulating user data in the database
    using SQLAlchemy. Provides functionality to query users by username or email,
    and to create new user records.

    Parameters
    ----------
    session : Session, optional
        An SQLAlchemy database session. If not provided, a new session is obtained from get_db_session().

    Methods
    -------
    get_user_by_username(username)
        Retrieves a user record from the database by username.

    get_user_by_email(email)
        Retrieves a user record from the database by email.

    create_user(username, hashed_password, email)
        Creates a new user record in the database.
    """

    def __init__(self, session=None):
        """
        Initialize the UserRepositoryImpl.

        Parameters
        ----------
        session : Session, optional
            An SQLAlchemy session. If not provided, uses get_db_session().
        """
        self.session = session or get_db_session()

    def get_user_by_username(self, username):
        """
        Retrieve a user from the database by their username.

        Parameters
        ----------
        username : str
            The username to search for.

        Returns
        -------
        User or None
            The User instance if found, otherwise None.
        """
        return self.session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email):
        """
        Retrieve a user from the database by their email address.

        Parameters
        ----------
        email : str
            The email address to search for.

        Returns
        -------
        User or None
            The User instance if found, otherwise None.
        """
        return self.session.query(User).filter_by(email=email).first()

    def create_user(self, username, hashed_password, email):
        """
        Create a new user record in the database.

        Parameters
        ----------
        username : str
            The username for the new user.
        hashed_password : str
            The hashed password for the new user.
        email : str
            The email address for the new user.

        Returns
        -------
        User
            The newly created User instance.
        """
        user = User(username=username, password_hash=hashed_password, email=email)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user