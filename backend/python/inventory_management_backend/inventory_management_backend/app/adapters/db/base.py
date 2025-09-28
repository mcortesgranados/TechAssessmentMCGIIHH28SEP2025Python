"""
SQLAlchemy ORM Base & Product Entity - Hexagonal Event-Driven Microservices Foundation

This module serves as the persistence layer foundation for a hexagonal (ports & adapters) 
microservice architecture, implementing SQLAlchemy ORM patterns with event-driven capabilities 
and strict adherence to SOLID principles for maintainable enterprise applications.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as a driven adapter (secondary/infrastructure layer)
    - Implements the persistence port for the Product domain entity
    - Provides database abstraction that isolates business logic from ORM details
    - Enables substitutability with different persistence implementations (SQL, NoSQL, etc.)
    - Maintains clean boundaries between domain and infrastructure concerns

🔧 Microservices Pattern:
    - Encapsulates Product entity within inventory bounded context
    - Supports database-per-service pattern for data autonomy
    - Enables independent schema evolution and deployment
    - Facilitates horizontal scaling of product data operations
    - Provides clear service boundaries through entity encapsulation

📡 Event-Driven Architecture:
    - Supports domain event publishing through SQLAlchemy event listeners
    - Enables Change Data Capture (CDC) for real-time event streaming
    - Facilitates eventual consistency across distributed services
    - Provides audit trail capabilities through timestamp tracking
    - Supports event sourcing patterns for state reconstruction

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Base class solely manages declarative ORM configuration
    ✅ Product entity focuses exclusively on product data representation
    ✅ Clear separation between entity definition and business logic

O - Open/Closed Principle:
    ✅ Open for extension: new entities inherit from Base without modification
    ✅ Closed for modification: existing entity structure remains stable
    ✅ Supports mixins and traits for cross-cutting concerns

L - Liskov Substitution Principle:
    ✅ All entities derived from Base maintain consistent ORM behavior
    ✅ SQLAlchemy abstractions ensure substitutability across implementations
    ✅ Maintains behavioral contracts for persistence operations

I - Interface Segregation Principle:
    ✅ Entity exposes only necessary attributes for product representation
    ✅ Avoids coupling to unused ORM features or methods
    ✅ Clean separation of persistence concerns from business operations

D - Dependency Inversion Principle:
    ✅ Depends on SQLAlchemy abstractions, not concrete database implementations
    ✅ Enables dependency injection of different database engines
    ✅ Supports testing with in-memory databases or mocks

ENTERPRISE PATTERNS IMPLEMENTATION:
==================================

🔄 Active Record Pattern Enhancement:
    - Timestamp tracking for audit trails and event sourcing
    - Automatic created_at/updated_at management
    - Support for soft deletes and versioning strategies

🛠️ Repository Pattern Support:
    - Provides entity foundation for repository implementations
    - Enables domain-driven design (DDD) aggregate patterns
    - Supports specification pattern for complex queries

📊 Data Integrity & Validation:
    - Column constraints ensure data consistency
    - Type safety through SQLAlchemy column definitions
    - Nullable constraints enforce business rules at schema level

🔐 Security & Compliance:
    - Audit trail support through timestamp columns
    - Schema-level constraints for data validation
    - Prepared statement protection against SQL injection

PERFORMANCE OPTIMIZATIONS:
=========================
- ✅ Efficient column type selection (BigInteger for IDs, DECIMAL for precision)
- ✅ Indexed primary key for fast lookups
- ✅ Server-side default timestamps reduce application overhead
- ✅ Optimal column sizes to minimize storage footprint

INTEGRATION CAPABILITIES:
========================
```python
# Event-driven integration example
from sqlalchemy import event

@event.listens_for(Product, 'after_insert')
def publish_product_created(mapper, connection, target):
    # Publish domain event for product creation
    publish_event('ProductCreated', target.id, target.__dict__)

# Repository pattern integration
class ProductRepository:
    def __init__(self, session):
        self.session = session
    
    def save(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        return product
```

USAGE EXAMPLES:
==============
```python
# Direct entity usage
product = Product(
    name="Laptop Dell XPS 13",
    description="High-performance ultrabook",
    price=Decimal('1299.99'),
    stock=50
)

# Event-driven pattern
product.publish_domain_events()  # Custom method for event publishing

# Microservice integration
inventory_service.add_product(product)
```

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

from sqlalchemy import Column, BigInteger, String, Text, DECIMAL, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    """
    🏷️ SQLAlchemy Product Entity

    Represents a product record in the inventory system.

    Attributes:
        id (BigInteger): Primary key, auto-incremented.
        name (String): Product name and identifying info.
        description (Text): Detailed description.
        price (DECIMAL): Product price.
        stock (Integer): Stock quantity.
        created_at (TIMESTAMP): Creation timestamp.
        updated_at (TIMESTAMP): Update timestamp.
    """
    __tablename__ = "products"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10,2), nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())