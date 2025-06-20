import logging
from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from products_cli_tryout.config.db import db, Database
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

    def clear_all_products(self) -> None:
        """Delete all products from the table"""
        try:
            with self.db.get_session() as session:
                session.query(Product).delete()
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error clearing all products: {str(e)}")
            raise ProductError(f"Failed to clear all products: {str(e)}")

    def get_products_paginated(self, page: int = 1, page_size: int = 10) -> List[Product]:
        """Get products paginated"""
        try:
            with self.db.get_session() as session:
                products = session.query(Product) \
                    .offset((page - 1) * page_size) \
                    .limit(page_size) \
                    .all()
                return products
        except SQLAlchemyError as e:
            logger.error(f"Error fetching paginated products: {str(e)}")
            raise ProductError(f"Failed to fetch paginated products: {str(e)}")

    def get_products_with_fields(self, fields: List[str]) -> List[dict]:
        """Get all products with only specified fields"""
        try:
            with self.db.get_session() as session:
                products = session.query(Product).all()
                result = []
                for product in products:
                    prod_dict = product.to_dict()
                    filtered = {field: prod_dict.get(field) for field in fields if field in prod_dict}
                    result.append(filtered)
                return result
        except SQLAlchemyError as e:
            logger.error(f"Error fetching products with fields: {str(e)}")
            raise ProductError(f"Failed to fetch products with fields: {str(e)}")

    def search_filter_sort_products(self, search: str = None, category: str = None, min_price: float = None, max_price: float = None, sort_by: str = None, sort_desc: bool = False) -> List[Product]:
        """Advanced search, filter, and sort for products"""
        try:
            with self.db.get_session() as session:
                query = session.query(Product)
                if search:
                    query = query.filter(Product.name.ilike(f"%{search}%"))
                if category:
                    query = query.filter(Product.category == category)
                if min_price is not None:
                    query = query.filter(Product.price >= min_price)
                if max_price is not None:
                    query = query.filter(Product.price <= max_price)
                if sort_by and hasattr(Product, sort_by):
                    sort_col = getattr(Product, sort_by)
                    if sort_desc:
                        sort_col = sort_col.desc()
                    query = query.order_by(sort_col)
                products = query.all()
                return products
        except SQLAlchemyError as e:
            logger.error(f"Error in search/filter/sort: {str(e)}")
            raise ProductError(f"Failed to search/filter/sort products: {str(e)}")

    def bulk_create_products(self, products_data: List[dict]) -> List[Product]:
        """Create multiple products with validation"""
        try:
            with self.db.get_session() as session:
                products = []
                for data in products_data:
                    # Validate using Product's validation
                    Product.validate_fields(
                        data['name'],
                        float(data['price']),
                        int(data['quantity']),
                        data.get('category')
                    )
                    products.append(Product.from_dict(data))
                session.add_all(products)
                session.commit()
                return products
        except SQLAlchemyError as e:
            logger.error(f"Error creating bulk products: {str(e)}")
            raise ProductError(f"Failed to create bulk products: {str(e)}")
        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}")
            raise ProductError(f"Validation error: {str(ve)}")


def create_product_service(db_bean: Database = db) -> ProductServiceInterface:
    return ProductService(db_bean)
