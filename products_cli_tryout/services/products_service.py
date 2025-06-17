import logging
from products_cli_tryout.db import Session
from products_cli_tryout.models.products import Product

logger = logging.getLogger(__name__)

class ProductError(Exception):
    """Base exception for product-related errors"""
    pass

class ProductNotFoundError(ProductError):
    """Raised when a product is not found"""
    pass

def insert_bulk_products(products):
    """
    Inserts a list of products into the database.

    :param products: List of Product objects to be inserted.
    """
    logger.info(f"Inserting {len(products)} products")
    session = Session()
    try:
        session.bulk_save_objects([Product(**product) for product in products])
        session.commit()
        logger.info("Products inserted successfully")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to insert products: {str(e)}")
        raise ProductError(f"Failed to insert products: {str(e)}")
    finally:
        session.close()

def get_all_products():
    """
    Retrieves all products from the database.

    :return: List of Product objects.
    """
    logger.info("Retrieving all products")
    session = Session()
    try:
        products = session.query(Product).all()
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Failed to retrieve products: {str(e)}")
        raise ProductError(f"Failed to retrieve products: {str(e)}")
    finally:
        session.close()

def delete_product_by_id(product_id):
    """
    Deletes a product by its ID.

    :param product_id: ID of the product to be deleted.
    """
    logger.info(f"Deleting product with ID: {product_id}")
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if not product:
            logger.warning(f"Product with ID {product_id} not found")
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        
        session.delete(product)
        session.commit()
        logger.info(f"Product {product_id} deleted successfully")
    except ProductNotFoundError:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to delete product {product_id}: {str(e)}")
        raise ProductError(f"Failed to delete product: {str(e)}")
    finally:
        session.close()