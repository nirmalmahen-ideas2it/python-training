import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class CSVError(Exception):
    """Base exception for CSV-related errors"""
    pass


class CSVFileNotFoundError(CSVError):
    """Raised when CSV file is not found"""
    pass


class CSVValidationError(CSVError):
    """Raised when CSV data validation fails"""
    pass


def read_csv(file_path):
    """
    Reads and validates data from a CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        List of product dictionaries
        
    Raises:
        CSVFileNotFoundError: If file doesn't exist
        CSVValidationError: If data validation fails
    """
    file_path = Path(file_path)
    if not file_path.exists():
        logger.error(f"CSV file not found: {file_path}")
        raise CSVFileNotFoundError(f"File {file_path} does not exist")

    products = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                try:
                    # Validate required fields
                    if not all(key in row for key in ['name', 'price', 'quantity']):
                        raise CSVValidationError("Missing required fields in CSV")

                    # Convert and validate numeric fields
                    try:
                        price = float(row['price'])
                        quantity = int(row['quantity'])
                        if price < 0 or quantity < 0:
                            raise CSVValidationError("Price and quantity must be non-negative")
                    except ValueError:
                        raise CSVValidationError("Invalid numeric values in CSV")

                    products.append({
                        "name": row["name"].strip(),
                        "description": row.get("description", "").strip(),
                        "price": price,
                        "quantity": quantity
                    })
                except CSVValidationError as e:
                    logger.error(f"Validation error in row: {str(e)}")
                    raise

        if not products:
            logger.warning("No valid products found in CSV file")
            raise CSVValidationError("No valid products found in CSV file")

        logger.info(f"Successfully read {len(products)} products from CSV")
        return products

    except csv.Error as e:
        logger.error(f"CSV parsing error: {str(e)}")
        raise CSVError(f"Failed to parse CSV file: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error reading CSV: {str(e)}")
        raise CSVError(f"Failed to read CSV file: {str(e)}")
