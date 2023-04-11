# Standard Libraries
from typing import Optional

# Third-party Libraries
from pydantic import BaseModel, validator


class BrandModel(BaseModel):
    name: str
    description: Optional[str] = None


class ProductModel(BrandModel):
    name: str
    price: float

    @validator("name")
    def check_sum(cls, v):
        if len(v) > 250:
            raise ValueError("max length of name is 250")
        return v
