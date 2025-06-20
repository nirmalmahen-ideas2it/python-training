from typing import Optional, Dict, Any

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

# Declarative base class for SQLAlchemy models
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(String(50), nullable=True)

    def __init__(self, name: str, price: float, quantity: int, description: Optional[str] = None, category: Optional[str] = None):
        self.validate_fields(name, price, quantity, category)
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.category = category

    @staticmethod
    def validate_fields(name, price, quantity, category):
        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a non-empty string.")
        if price is None or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Product price must be a non-negative number.")
        if quantity is None or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Product quantity must be a non-negative integer.")
        if category is not None and not isinstance(category, str):
            raise ValueError("Product category must be a string if provided.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create product instance from dictionary"""
        return cls(
            name=data['name'],
            price=float(data['price']),
            quantity=int(data['quantity']),
            description=data.get('description'),
            category=data.get('category')
        )

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity}, category='{self.category}')"
