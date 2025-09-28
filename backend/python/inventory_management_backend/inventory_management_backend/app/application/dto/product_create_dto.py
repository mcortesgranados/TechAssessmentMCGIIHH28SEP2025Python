from pydantic import BaseModel, Field
from typing import Optional

class ProductCreateDTO(BaseModel):
    """
    🎯 Data Transfer Object for product creation.

    Attributes:
        name (str): Product name.
        description (Optional[str]): Product description (nullable).
        price (float): Product price.
        quantity (int): Initial inventory quantity.
    """
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)