# Product CLI Application – Architecture & Technical Overview

---

## 1. High-Level Overview

This project is a **command-line interface (CLI) application** for managing products. Users interact with the app via terminal commands, providing inputs to perform various product-related operations (like add, update, delete, list, etc.).

---

## 2. Technical Architecture & Patterns

### a. Database Layer

- **Singleton Pattern for DB Connection**  
  The database connection is implemented as a singleton, ensuring only one instance of the DB connection exists throughout the application's lifecycle.
- **DB URL Configuration**  
  The database URL is fetched from a configuration variable (in `config.py`), making the DB connection flexible and environment-agnostic.

### b. Service Layer

- **Factory Pattern for Product Service**  
  The Product Service is constructed using the Factory Pattern.
- **Dependency Injection**  
  The DB connection is injected as a dependency into the Product Service. This allows the service to be decoupled from the specific DB implementation, enabling support for different types of databases by passing different DB connection objects during initialization.

### c. Modularity

- **Separation of Concerns**  
  - Models (in `models/products.py`) define the product data structure.
  - Services (in `services/products_service.py` and `services/csv_service.py`) encapsulate business logic for products and CSV operations.
  - The `main.py` file acts as the CLI entry point, orchestrating user input and invoking the appropriate services.

---

## 3. Business Logic & Features

### a. Product Management

- **CRUD Operations**  
  The application supports basic Create, Read, Update, and Delete (CRUD) operations for products.
- **CSV Integration**  
  There is a service for handling CSV files, allowing import/export of product data.

### b. CLI Interaction

- **User Input Handling**  
  The `main.py` file parses user commands and arguments, then routes them to the appropriate service methods.
- **Command Options**  
  Users can perform actions like adding a product, listing products, updating, deleting, and possibly importing/exporting via CSV.

---

## 4. File/Module Responsibilities

| File/Module                  | Responsibility                                                      |
|------------------------------|---------------------------------------------------------------------|
| `config.py`                  | Stores configuration variables (like DB URL)                        |
| `db.py`                      | Manages the database connection, likely as a singleton              |
| `models/products.py`         | Defines the Product data model                                      |
| `services/products_service.py`| Contains business logic for product operations, via factory pattern |
| `services/csv_service.py`    | Handles CSV import/export logic                                     |
| `main.py`                    | CLI entry point, handles user interaction and command routing       |

---

## 5. Extensibility

- **Database Agnostic**  
  By injecting the DB connection into the service, the app can support multiple DB backends (e.g., SQLite, PostgreSQL, etc.) with minimal changes.
- **Service Factory**  
  The use of a factory for service creation allows for easy extension to other services or DB types.

---

## 6. Example Flow

1. **User runs the CLI** and selects an operation (e.g., add product).
2. `main.py` parses the command and arguments.
3. The appropriate **service** is instantiated (with DB connection injected).
4. The service performs the requested operation, possibly interacting with the DB or CSV files.
5. **Output** is displayed to the user.

---

## 7. Summary Table

| Layer         | Pattern/Technique         | Key Details                                                      |
|---------------|--------------------------|------------------------------------------------------------------|
| DB            | Singleton                | One DB connection, URL from config                               |
| Service       | Factory, Dependency Injection | ProductService created with injected DB connection           |
| CLI           | Command Routing          | main.py parses and routes user commands                          |
| Extensibility | Decoupled, Modular       | Easy to swap DBs, add services, or extend features               |

---

## 8. New Features & Enhancements (Post-Initial Version)

### 1. Product Model Enhancements
- **Category Field**: The `Product` model now includes a `category` field, allowing products to be grouped and filtered by category.
- **Field Validation**: Input validation is enforced for all product fields (name, price, quantity, category).

### 2. Service Layer Enhancements
- **Clear All Products**: Added a method and CLI command to delete all products from the database, with user confirmation.
- **Paginated Listing**: Users can now list products page by page, specifying page size and continuing interactively until all products are viewed.
- **Selective Field Display**: Users can choose which product fields to display (e.g., only name and quantity).
- **Advanced Search, Filter, and Sort**: CLI and service support searching by name, filtering by category and price range, and sorting by any field (ascending/descending).

### 3. CLI/UX Improvements
- **Interactive Pagination**: After each page, users are prompted to continue or exit, making it easy to browse large datasets.
- **Expanded Menu**: The CLI menu now includes options for all new features, including advanced search and field selection.

### 4. Security & Configuration
- **Vault Integration for DB Credentials**: Database username and password are now securely fetched from a Vault server at runtime using a token, rather than being stored in files.
- **Runtime Environment Variables**: The application supports passing sensitive information (like Vault tokens) as environment variables at runtime, never writing them to disk.

### 5. Testing & Quality Assurance
- **Unit Tests**: Added pytest-based unit tests for the enhanced service layer, covering creation, validation, pagination, field selection, and advanced querying.

### 6. Logging Setup as a Decorator
- **Logging Decorator**: The logging setup can now be applied as a decorator to entry points, ensuring logging is configured before any main logic runs.

### Summary Table of New Features

| Area                | New Feature/Enhancement                                      |
|---------------------|-------------------------------------------------------------|
| Product Model       | Category field, input validation                            |
| Service Layer       | Clear all, paginated listing, selective fields, search/filter/sort |
| CLI/UX              | Interactive pagination, expanded menu, field selection      |
| Security/Config     | Vault integration, runtime env vars for secrets             |
| Testing             | Pytest-based unit tests for all new features                |
| Logging             | Logging setup as a reusable decorator                       |

---

## 9. Potential Future Enhancements

- **User Authentication & Roles:** Implement user login and role-based permissions for secure and controlled access.
- **Product Update Support:** Add the ability to update product details directly from the CLI.
- **Data Export:** Allow exporting product data to CSV, JSON, or Excel for reporting and backup.
- **Audit Logging:** Track all product changes with detailed audit logs for compliance and traceability.

If you want a more detailed breakdown of any specific file, class, or function, or a diagram of the architecture, see the codebase or request further documentation. 