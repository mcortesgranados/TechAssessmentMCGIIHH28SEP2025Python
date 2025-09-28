from app.domain.services.user_service import UserService
from app.application.dto.user_dto import UserCreateDTO

def register_user_use_case(user_in: UserCreateDTO, user_service: UserService):
    """
    Application Service (Use Case):
    Orchestrates user registration workflow.
    Coordinates domain service and additional steps.
    """
    # Example: you could trigger an event, send email here, etc.
    user = user_service.register_user(user_in)
    # Optionally publish event, audit, etc.
    return user# register_user.py
