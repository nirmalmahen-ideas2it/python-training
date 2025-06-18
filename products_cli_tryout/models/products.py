from typing import Optional, Dict, Any

from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

# Declarative base class for SQLAlchemy models
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __init__(self, name: str, price: float, quantity: int, description: Optional[str] = None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create product instance from dictionary"""
        return cls(
            name=data['name'],
            price=float(data['price']),
            quantity=int(data['quantity']),
            description=data.get('description')
        )

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})"
