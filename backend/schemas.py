from pydantic import BaseModel, PositiveFloat, PositiveInt, EmailStr, validator
from enum import Enum
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    """
    Denominador comum entre 
    o Create, Read e Update.
    """
    name: str
    description: str
    price: PositiveFloat
    category: str
    supplier_email: EmailStr


class ProductCreate(ProductBase):
    # Exatamente igual ao ProductBase
    pass


class ProductRead(ProductBase):
    id: PositiveInt
    created_at: datetime

    class Config:
        from_atributes = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    category: Optional[str] = None
    supplier_email: Optional[EmailStr] = None
