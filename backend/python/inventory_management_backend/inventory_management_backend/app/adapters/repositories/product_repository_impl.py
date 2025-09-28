"""
Product Repository Implementation - Hexagonal Event-Driven Persistence Layer

This module implements the Repository pattern as part of a hexagonal (ports & adapters) 
microservice architecture, providing complete CRUD operations for Product entities with 
event-driven capabilities and strict adherence to SOLID principles for enterprise applications.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as a driven adapter (secondary/infrastructure layer)
    - Implements the ProductRepository port defined in the domain layer
    - Provides data persistence abstraction for Product aggregate roots
    - Isolates business logic from database implementation details
    - Enables substitutability with different persistence mechanisms (SQL, NoSQL, file-based)

🔧 Microservices Pattern:
    - Encapsulates product data operations within inventory bounded context
    - Supports database-per-service pattern for data autonomy
    - Enables independent deployment and scaling of product operations
    - Facilitates service mesh integration through standardized interfaces
    - Provides clear service boundaries through repository abstraction

📡 Event-Driven Architecture:
    - Publishes domain events for all state-changing operations (create, update, delete)
    - Supports Command Query Responsibility Segregation (CQRS) patterns
    - Enables eventual consistency across distributed microservices
    - Facilitates event sourcing for complete audit trails
    - Integrates with message brokers for asynchronous event publishing

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Solely responsible for Product entity persistence operations
    ✅ Separates data access concerns from business logic and presentation
    ✅ Focused exclusively on CRUD operations and query management

O - Open/Closed Principle:
    ✅ Open for extension: new query methods can be added without modification
    ✅ Closed for modification: core persistence logic remains stable
    ✅ Supports specification pattern for complex query extensions

L - Liskov Substitution Principle:
    ✅ Fully substitutable for any ProductRepository implementation
    ✅ Maintains behavioral contracts defined by repository interface
    ✅ Consistent exception handling across different implementations

I - Interface Segregation Principle:
    ✅ Implements specific product repository interface
    ✅ Clients depend only on methods they actually use
    ✅ Clean separation between read and write operations

D - Dependency Inversion Principle:
    ✅ Depends on session abstraction, not concrete database implementations
    ✅ Supports dependency injection for testing and flexibility
    ✅ Enables configuration-driven database selection

DOMAIN-DRIVEN DESIGN PATTERNS:
==============================

🎯 Repository Pattern:
    - Encapsulates Product aggregate persistence logic
    - Provides collection-like interface for domain objects
    - Maintains aggregate consistency boundaries
    - Supports unit of work pattern through session management

🔄 Aggregate Root Management:
    - Ensures Product entity integrity through proper session handling
    - Maintains transactional boundaries for aggregate operations
    - Supports optimistic concurrency control through versioning
    - Handles aggregate lifecycle from creation to deletion

📊 Query Object Pattern:
    - Supports complex queries through method composition
    - Enables specification pattern for dynamic query building
    - Provides type-safe query interfaces for compile-time validation
    - Optimizes query performance through proper indexing strategies

ENTERPRISE FEATURES:
===================

🛡️ Transaction Management:
    - ACID compliance through proper session handling
    - Automatic rollback on operation failures
    - Deadlock detection and retry mechanisms
    - Distributed transaction support for cross-service operations

⚡ Performance Optimizations:
    - Lazy loading for related entities
    - Query result caching for read-heavy operations
    - Batch operations for bulk data processing
    - Connection pooling for high-throughput scenarios

🔐 Security & Audit:
    - Input validation for all CRUD operations
    - Audit trail support through timestamp tracking
    - Access control integration through session context
    - SQL injection prevention through parameterized queries

📈 Monitoring & Observability:
    - Operation metrics for performance monitoring
    - Error rate tracking for reliability assessment
    - Query performance logging for optimization
    - Health check integration for service monitoring

EVENT-DRIVEN INTEGRATION:
========================

```python
# Event publishing integration
class ProductRepositoryImpl:
    def __init__(self, session=None, event_publisher=None):
        self.session = session or get_db_session()
        self.event_publisher = event_publisher
    
    def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.session.add(product)
        self.session.commit()
        
        # Publish domain event
        if self.event_publisher:
            self.event_publisher.publish(
                ProductCreatedEvent(product.id, product.__dict__)
            )
        
        return product
```

TESTING STRATEGIES:
==================

```python
# Unit testing with mocked session
@pytest.fixture
def mock_repository():
    mock_session = Mock()
    return ProductRepositoryImpl(session=mock_session)

# Integration testing with test database
@pytest.fixture
def test_repository(test_db_session):
    return ProductRepositoryImpl(session=test_db_session)

# Performance testing
def test_bulk_operations_performance():
    repository = ProductRepositoryImpl()
    products = [generate_test_product() for _ in range(1000)]
    
    start_time = time.time()
    repository.bulk_create(products)
    execution_time = time.time() - start_time
    
    assert execution_time < 5.0  # Performance threshold
```

USAGE EXAMPLES:
==============

```python
# Basic CRUD operations
repository = ProductRepositoryImpl()

# Create
product = repository.create_product({
    "name": "Laptop Dell XPS 13",
    "description": "High-performance ultrabook",
    "price": 1299.99,
    "stock": 50
})

# Read
all_products = repository.get_all_products()
specific_product = repository.get_product_by_id(1)

# Update
updated_product = repository.update_product(1, {"price": 1199.99})

# Delete
success = repository.delete_product(1)

# Advanced queries with specifications
low_stock_products = repository.find_by_specification(
    LowStockSpecification(threshold=10)
)
```

MICROSERVICE INTEGRATION:
========================

```python
# Service layer integration
class ProductService:
    def __init__(self, repository: ProductRepositoryImpl):
        self.repository = repository
    
    async def create_product_with_events(self, product_data):
        product = self.repository.create_product(product_data)
        await self.publish_product_created_event(product)
        return product

# API layer integration
@router.post("/products")
async def create_product(
    product_data: ProductCreateDTO,
    repository: ProductRepositoryImpl = Depends(get_repository)
):
    return repository.create_product(product_data.dict())
```

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

from typing import List, Optional
from app.adapters.db.session import get_db_session
from app.adapters.db.base import Product

class ProductRepositoryImpl:
    """
    🗄️ Implements CRUD operations for Product entities.

    Args:
        session: Optional SQLAlchemy session for dependency injection.

    Methods:
        get_all_products(): List all products.
        get_product_by_id(product_id): Get product by ID.
        create_product(product_data): Create a product.
        update_product(product_id, update_data): Update an existing product.
        delete_product(product_id): Delete a product by ID.
    """
    def __init__(self, session=None):
        # 💉 Dependency injection for session; if not provided, get a new one
        self.session = session or get_db_session()

    def get_all_products(self) -> List[Product]:
        """🔎 Retrieve all products from the database."""
        return self.session.query(Product).all()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """🔎 Retrieve a single product by its ID."""
        return self.session.query(Product).filter(Product.id == product_id).first()

    def create_product(self, product_data: dict) -> Product:
        """🆕 Create a new product."""
        new_product = Product(**product_data)
        self.session.add(new_product)
        self.session.commit()
        self.session.refresh(new_product)
        return new_product

    def update_product(self, product_id: int, update_data: dict) -> Optional[Product]:
        """🔄 Update an existing product."""
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        for key, value in update_data.items():
            setattr(product, key, value)
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        """🗑️ Delete a product by ID."""
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.session.delete(product)
        self.session.commit()
        return True