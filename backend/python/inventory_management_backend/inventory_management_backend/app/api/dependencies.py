from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.adapters.auth.jwt_manager import JWTManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    print(f"Received token in FastAPI: {token}")  # Add this line
    try:
        payload = JWTManager.verify_access_token(token)
        print(f"Decoded payload: {payload}")      # And this
        return payload
    except Exception as e:
        print(f"JWT error: {e}")                  # And this
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )