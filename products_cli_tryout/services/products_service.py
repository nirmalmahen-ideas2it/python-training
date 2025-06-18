import logging
from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from products_cli_tryout.db import db, Database
from products_cli_tryout.models.products import Product

logger = logging.getLogger(__name__)


class ProductError(Exception):
    """Base exception for product-related errors"""
    pass


class ProductNotFoundError(ProductError):
    """Exception raised when a product is not found"""
    pass


class ProductServiceInterface(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

    @abstractmethod
    def bulk_create_products(self, products_data: List[dict]) -> List[Product]:
        pass


class ProductService(ProductServiceInterface):
    def __init__(self, db_bean: Database):
        self.db = db_bean

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        try:
            with self.db.get_session() as session:
                products = session.query(Product).all()
                return products  # Ensure to_dict() is implemented
        except SQLAlchemyError as e:
            logger.error(f"Error fetching products: {str(e)}")
            raise ProductError(f"Failed to fetch products: {str(e)}")

    def delete_product(self, product_id: int) -> None:
        """Delete a product by ID"""
        try:
            with self.db.get_session() as session:
                product = session.query(Product).filter(Product.id == product_id).first()
                if not product:
                    raise ProductNotFoundError(f"Product with ID {product_id} not found")
                session.delete(product)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting product {product_id}: {str(e)}")
            raise ProductError(f"Failed to delete product: {str(e)}")

    def bulk_create_products(self, products_data: List[dict]) -> List[Product]:
        """Create multiple products"""
        try:
            with self.db.get_session() as session:
                products = [Product.from_dict(data) for data in products_data]
                session.add_all(products)
                session.commit()
                return products
        except SQLAlchemyError as e:
            logger.error(f"Error creating bulk products: {str(e)}")
            raise ProductError(f"Failed to create bulk products: {str(e)}")


def create_product_service(db_bean: Database = db) -> ProductServiceInterface:
    return ProductService(db_bean)
