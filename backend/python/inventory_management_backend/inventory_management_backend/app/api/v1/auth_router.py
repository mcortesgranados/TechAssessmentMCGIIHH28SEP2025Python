from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.application.services.user_application_service import UserApplicationService
from app.adapters.auth.jwt_manager import JWTManager
from app.application.dto.user_dto import TokenDTO, UserCreateDTO, UserDTO

router = APIRouter(prefix="/auth", tags=["auth"])

user_service = UserApplicationService()

@router.post("/login", response_model=TokenDTO)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return JWT token.
    """
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = JWTManager.create_access_token({"sub": user.username})
    return TokenDTO(access_token=access_token)

@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreateDTO):
    """
    Register a new user.
    """
    try:
        user = user_service.register_user(user_in)
        return UserDTO.from_model(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))