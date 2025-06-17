from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

# Declarative base class for SQLAlchemy models
Base=declarative_base()

class Product(Base):
    __tablename__='products_tryout'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Integer, index=True)
