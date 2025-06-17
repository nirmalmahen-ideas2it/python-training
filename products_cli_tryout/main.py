import logging

from products_cli_tryout.config import setup_logging
from products_cli_tryout.db import engine
from products_cli_tryout.models.products import Base
from products_cli_tryout.services.products_service import (
    insert_bulk_products,
    get_all_products,
    delete_product_by_id,
    ProductError,
    ProductNotFoundError
)
from products_cli_tryout.services.csv_service import (
    read_csv,
    CSVFileNotFoundError,
    CSVValidationError,
    CSVError
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

def display_products(products):
    """Display products in a simple format"""
    if not products:
        print("No products found.")
        return

    print("\nProducts:")
    print("-" * 80)
    print(f"{'ID':<5} {'Name':<20} {'Description':<30} {'Price':<10} {'Quantity':<10}")
    print("-" * 80)
    
    for product in products:
        print(f"{product.id:<5} {product.name:<20} {product.description or '':<30} "
              f"${product.price:<9.2f} {product.quantity:<10}")

def upload_csv_file():
    """Handle CSV file upload"""
    file_path = input("Enter the path to the CSV file: ")
    
    try:
        # Confirm upload
        confirm = input(f"Are you sure you want to upload products from {file_path}? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

        print("Reading CSV file...")
        products_data = read_csv(file_path)
        
        print("Uploading products...")
        insert_bulk_products(products_data)
        print(f"Successfully uploaded {len(products_data)} products.")

    except (CSVError,CSVFileNotFoundError, CSVValidationError) as e:
        print(f"Error: {str(e)}")
    except ProductError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during CSV upload: {str(e)}")
        print("An unexpected error occurred. Check the logs for details.")

def list_all_products():
    """Display all products"""
    try:
        products = get_all_products()
        display_products(products)
        print(f"\nFound {len(products)} products.")

    except ProductError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error while listing products: {str(e)}")
        print("An unexpected error occurred. Check the logs for details.")

def delete_product():
    """Handle product deletion"""
    try:
        product_id = int(input("Enter product ID to delete: "))
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete product {product_id}? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return

        delete_product_by_id(product_id)
        print(f"Successfully deleted product {product_id}.")

    except ValueError:
        print("Error: Please enter a valid product ID (number).")
    except ProductNotFoundError as e:
        print(f"Error: {str(e)}")
    except ProductError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error while deleting product: {str(e)}")
        print("An unexpected error occurred. Check the logs for details.")

def main():
    """Main application loop"""
    while True:
        print("\nProducts CLI Management Tool")
        print("1. Upload CSV file with products")
        print("2. List all products")
        print("3. Delete product by ID")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            upload_csv_file()
        elif choice == "2":
            list_all_products()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


