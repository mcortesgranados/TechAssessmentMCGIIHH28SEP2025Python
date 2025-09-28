from pydantic import BaseModel, Field
from typing import Optional

class ProductUpdateDTO(BaseModel):
    """
    🎯 Data Transfer Object for product updates.

    All fields are optional for partial updates.
    Example values are provided for Swagger testing.
    """
    name: Optional[str] = Field(
        None, min_length=1, max_length=200, example="Webcam Apple High quality PR40766"
    )
    description: Optional[str] = Field(
        None, max_length=1000, example="High quality by Apple, reference PR40766"
    )
    price: Optional[float] = Field(
        None, gt=0, example=1845.38
    )
    stock: Optional[int] = Field(
        None, ge=0, example=500
    )