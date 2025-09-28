from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class TokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreateDTO(BaseModel):
    username: str
    password: str
    email: EmailStr

    @field_validator('password')
    def password_length_check(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError("Password cannot be longer than 72 bytes")
        return v

class UserDTO(BaseModel):
    id: int
    username: str
    email: EmailStr

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            username=model.username,
            email=model.email
        )