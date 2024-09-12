from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)
    supplier_email = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
