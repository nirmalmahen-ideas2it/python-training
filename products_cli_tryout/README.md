# Products CLI Management Tool

A simple command-line interface (CLI) tool for managing products, built with Python and SQLAlchemy.

## Features

- Upload products from CSV files
- List all products
- Delete products
- Error handling and logging
- Data validation

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database

## Installation

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
LOG_LEVEL=INFO
```

## Usage

The CLI provides the following commands:

### Upload Products from CSV

```bash
python -m products_cli_tryout upload-csv path/to/products.csv
```

The CSV file should have the following columns:

- name (required)
- description (optional)
- price (required, must be positive)
- quantity (required, must be non-negative)

### List All Products

```bash
python -m products_cli_tryout list-products
```

### Delete Product

```bash
python -m products_cli_tryout delete-product <product-id>
```

Add `--force` or `-f` to skip confirmation.

## Project Structure

```
products_cli_tryout/
├── config.py           # Configuration management
├── db.py              # Database connection management
├── main.py            # CLI application
├── models/
│   └── products.py    # Database models
└── services/
    ├── products_service.py  # Product operations
    └── csv_service.py       # CSV file handling
```

## Error Handling

The application includes error handling for:

- Database connection issues
- Invalid CSV data
- Missing or invalid product data
- File system errors

All errors are logged with appropriate context and user-friendly error messages are displayed.

## Logging

Logs can be stored in `<file_name>.log`. The log level can be configured in the `.env` file. 