import logging
from typing import List

from products_cli_tryout.config.config import setup_logging
from products_cli_tryout.config.db import db as postgres_db
from products_cli_tryout.config.config import logger as logger_decorator
from products_cli_tryout.models.products import Base, Product
from products_cli_tryout.services.csv_service import (
    read_csv,
    CSVFileNotFoundError,
    CSVValidationError,
    CSVError
)
from products_cli_tryout.services.products_service import (
    create_product_service,
    ProductError,
    ProductNotFoundError
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=postgres_db.engine)


class ProductCLI:
    def __init__(self):
        self.product_service = create_product_service(postgres_db)

    @logger_decorator
    def display_products(self, products: List[Product], fields: List[str] = None) -> None:
        """Display products in a simple format, optionally with selected fields"""
        if not products:
            print("No products found.")
            return

        if fields:
            # Display only requested fields
            print("\nProducts:")
            print("-" * 80)
            header = ' '.join([f"{field.capitalize():<15}" for field in fields])
            print(header)
            print("-" * 80)
            for product in products:
                if isinstance(product, dict):
                    row = ' '.join([str(product.get(field, ''))[:15].ljust(15) for field in fields])
                else:
                    prod_dict = product.to_dict()
                    row = ' '.join([str(prod_dict.get(field, ''))[:15].ljust(15) for field in fields])
                print(row)
        else:
            print("\nProducts:")
            print("-" * 100)
            print(f"{'ID':<5} {'Name':<20} {'Description':<30} {'Price':<10} {'Quantity':<10} {'Category':<15}")
            print("-" * 100)
            for product in products:
                print(f"{product.id:<5} {product.name:<20} {product.description or '':<30} "
                      f"${product.price:<9.2f} {product.quantity:<10} {getattr(product, 'category', ''):<15}")

    @logger_decorator
    def upload_csv_file(self) -> None:
        """Handle CSV file upload"""
        file_path = input("Enter the path to the CSV file: ").strip()

        try:
            # Confirm upload
            confirm = input(f"Are you sure you want to upload products from {file_path}? (y/n): ").strip()
            if confirm.lower() != 'y':
                print("Operation cancelled.")
                return

            print("Reading CSV file...")
            products_data = read_csv(file_path)

            print("Uploading products...")
            self.product_service.bulk_create_products(products_data)
            print(f"Successfully uploaded {len(products_data)} products.")

        except (CSVError, CSVFileNotFoundError, CSVValidationError) as e:
            print(f"Error: {str(e)}")
        except ProductError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during CSV upload: {str(e)}")
            print("An unexpected error occurred. Check the logs for details.")

    @logger_decorator
    def list_all_products(self) -> None:
        """Display all products"""
        try:
            products = self.product_service.get_all_products()
            self.display_products(products)
            print(f"\nFound {len(products)} products.")

        except ProductError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error while listing products: {str(e)}")
            print("An unexpected error occurred. Check the logs for details.")

    @logger_decorator
    def delete_product(self) -> None:
        """Handle product deletion"""
        try:
            product_id = int(input("Enter product ID to delete: ")).strip()

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete product {product_id}? (y/n): ")
            if confirm.lower().strip() != 'y':
                print("Operation cancelled.")
                return

            self.product_service.delete_product(product_id)
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

    @logger_decorator
    def clear_all_products(self) -> None:
        """Clear all products from the table"""
        confirm = input("Are you sure you want to delete ALL products? This cannot be undone. (y/n): ")
        if confirm.lower().strip() != 'y':
            print("Operation cancelled.")
            return
        try:
            self.product_service.clear_all_products()
            print("All products have been deleted.")
        except Exception as e:
            print(f"Error: {str(e)}")

    @logger_decorator
    def list_products_paginated(self) -> None:
        try:
            page = int(input("Enter page number to start (default 1): ").strip() or 1)
            page_size = int(input("Enter page size (default 10): ").strip() or 10)
            while True:
                products = self.product_service.get_products_paginated(page, page_size)
                if not products:
                    if page == 1:
                        print("No products found.")
                    else:
                        print("No more products.")
                    break
                self.display_products(products)
                print(f"\nDisplayed {len(products)} products on page {page}.")
                if len(products) < page_size:
                    print("No more products.")
                    break
                cont = input("Continue to next page? (y/n): ").strip().lower()
                if cont != 'y':
                    break
                page += 1
        except Exception as e:
            print(f"Error: {str(e)}")

    @logger_decorator
    def list_products_with_fields(self) -> None:
        try:
            fields = input("Enter comma-separated fields to display (e.g., name,quantity): ").strip().split(',')
            fields = [f.strip() for f in fields if f.strip()]
            if not fields:
                print("No fields specified.")
                return
            products = self.product_service.get_products_with_fields(fields)
            self.display_products(products, fields=fields)
            print(f"\nDisplayed {len(products)} products with fields: {', '.join(fields)}.")
        except Exception as e:
            print(f"Error: {str(e)}")

    @logger_decorator
    def search_filter_sort_products(self) -> None:
        try:
            search = input("Search by name (press Enter to skip): ").strip() or None
            category = input("Filter by category (press Enter to skip): ").strip() or None
            min_price = input("Minimum price (press Enter to skip): ").strip()
            min_price = float(min_price) if min_price else None
            max_price = input("Maximum price (press Enter to skip): ").strip()
            max_price = float(max_price) if max_price else None
            sort_by = input("Sort by field (name, price, quantity, category) (press Enter to skip): ").strip() or None
            sort_desc = input("Sort descending? (y/n, default n): ").strip().lower() == 'y'
            products = self.product_service.search_filter_sort_products(
                search=search,
                category=category,
                min_price=min_price,
                max_price=max_price,
                sort_by=sort_by,
                sort_desc=sort_desc
            )
            self.display_products(products)
            print(f"\nFound {len(products)} products matching criteria.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def run(self) -> None:
        """Main application loop"""
        while True:
            print("\nProducts CLI Management Tool")
            print("1. Upload CSV file with products")
            print("2. List all products")
            print("3. Delete product by ID")
            print("4. Clear all products")
            print("5. List products (paginated)")
            print("6. List products with selected fields")
            print("7. Search/Filter/Sort products")
            print("8. Exit")

            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == "1":
                self.upload_csv_file()
            elif choice == "2":
                self.list_all_products()
            elif choice == "3":
                self.delete_product()
            elif choice == "4":
                self.clear_all_products()
            elif choice == "5":
                self.list_products_paginated()
            elif choice == "6":
                self.list_products_with_fields()
            elif choice == "7":
                self.search_filter_sort_products()
            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")


def main():
    """Entry point of the application"""
    cli = ProductCLI()
    cli.run()


if __name__ == "__main__":
    main()
