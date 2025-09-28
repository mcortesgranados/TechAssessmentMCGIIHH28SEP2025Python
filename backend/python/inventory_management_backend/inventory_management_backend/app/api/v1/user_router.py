# user_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from app.application.dto.user_dto import UserCreateDTO, UserDTO
from app.domain.services.user_service import UserService
from app.adapters.repositories.user_repository_impl import UserRepositoryImpl

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def get_user_service():
    repo = UserRepositoryImpl()
    return UserService(repo)

@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def register_user(
    user_in: UserCreateDTO,
    service: UserService = Depends(get_user_service)
):
    """
    Register a new user.
    """
    try:
        user = service.register_user(user_in)
        return UserDTO.from_model(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))