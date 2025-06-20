import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from products_cli_tryout.models.products import Base, Product
from products_cli_tryout.services.products_service import ProductService
from products_cli_tryout.db import Database

class InMemoryDB(Database):
    def _initialize(self):
        if self._engine is None:
            self._engine = create_engine('sqlite:///:memory:')
            self._Session = sessionmaker(bind=self._engine, expire_on_commit=False)
            Base.metadata.create_all(self._engine)

def product_service():
    db = InMemoryDB()
    return ProductService(db)

@pytest.fixture
def service():
    return product_service()

def test_create_and_bulk_create_products(service):
    # Valid product
    p = Product(name='Test', price=10.0, quantity=5, description='desc', category='cat')
    assert p.name == 'Test'
    # Bulk create
    data = [
        {'name': 'A', 'price': 1.0, 'quantity': 1, 'description': 'd', 'category': 'c'},
        {'name': 'B', 'price': 2.0, 'quantity': 2, 'description': 'd2', 'category': 'c2'}
    ]
    products = service.bulk_create_products(data)
    assert len(products) == 2
    # Validation error
    with pytest.raises(Exception):
        service.bulk_create_products([{'name': '', 'price': -1, 'quantity': -1}])

def test_clear_all_products(service):
    data = [
        {'name': 'C', 'price': 3.0, 'quantity': 3, 'description': 'd3', 'category': 'c3'}
    ]
    service.bulk_create_products(data)
    service.clear_all_products()
    assert service.get_all_products() == []

def test_get_products_paginated(service):
    data = [
        {'name': f'P{i}', 'price': i, 'quantity': i, 'description': f'd{i}', 'category': 'cat'} for i in range(1, 21)
    ]
    service.bulk_create_products(data)
    page1 = service.get_products_paginated(page=1, page_size=5)
    page2 = service.get_products_paginated(page=2, page_size=5)
    assert len(page1) == 5
    assert len(page2) == 5
    assert page1[0].name == 'P1'
    assert page2[0].name == 'P6'

def test_get_products_with_fields(service):
    data = [
        {'name': 'F1', 'price': 1, 'quantity': 1, 'description': 'd', 'category': 'cat'}
    ]
    service.bulk_create_products(data)
    fields = ['name', 'quantity']
    result = service.get_products_with_fields(fields)
    assert result[0]['name'] == 'F1'
    assert result[0]['quantity'] == 1
    assert 'price' not in result[0]

def test_search_filter_sort_products(service):
    data = [
        {'name': 'Alpha', 'price': 10, 'quantity': 1, 'description': 'd', 'category': 'A'},
        {'name': 'Beta', 'price': 20, 'quantity': 2, 'description': 'd', 'category': 'B'},
        {'name': 'Gamma', 'price': 15, 'quantity': 3, 'description': 'd', 'category': 'A'}
    ]
    service.bulk_create_products(data)
    # Search
    results = service.search_filter_sort_products(search='Al')
    assert len(results) == 1 and results[0].name == 'Alpha'
    # Filter by category
    results = service.search_filter_sort_products(category='A')
    assert len(results) == 2
    # Price range
    results = service.search_filter_sort_products(min_price=12, max_price=18)
    assert len(results) == 1 and results[0].name == 'Gamma'
    # Sort by price desc
    results = service.search_filter_sort_products(sort_by='price', sort_desc=True)
    assert results[0].name == 'Beta' 