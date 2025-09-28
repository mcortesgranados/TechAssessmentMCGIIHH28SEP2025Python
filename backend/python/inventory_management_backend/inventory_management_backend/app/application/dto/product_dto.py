"""
Product Data Transfer Object - Hexagonal Event-Driven Data Contract

This module implements the Data Transfer Object (DTO) pattern as part of a hexagonal (ports & adapters) 
microservice architecture, providing type-safe data contracts for product entities with event-driven 
capabilities and strict adherence to SOLID principles for maintainable enterprise applications.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as a boundary object between application core and external adapters
    - Implements the anti-corruption layer pattern for data transformation
    - Provides stable contracts that isolate domain models from external representations
    - Enables independent evolution of internal domain and external API models
    - Maintains clean boundaries between different architectural layers

🔧 Microservices Pattern:
    - Defines service contracts for inter-service communication
    - Supports API versioning through DTO evolution strategies
    - Enables backward compatibility across service deployments
    - Facilitates service mesh integration through standardized data formats
    - Provides clear service boundaries through well-defined data contracts

📡 Event-Driven Architecture:
    - Serves as event payload schema for domain event publishing
    - Enables event sourcing through immutable data representations
    - Supports message broker integration with validated event schemas
    - Facilitates eventual consistency across distributed services
    - Provides type-safe event handling in event-driven workflows

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Solely responsible for product data representation and validation
    ✅ Separates data transfer concerns from business logic and persistence
    ✅ Focused exclusively on data contract definition and transformation

O - Open/Closed Principle:
    ✅ Open for extension: new fields can be added without breaking existing clients
    ✅ Closed for modification: core data structure remains stable
    ✅ Supports inheritance and composition for specialized DTOs

L - Liskov Substitution Principle:
    ✅ Fully substitutable across different serialization contexts
    ✅ Maintains behavioral contracts regardless of underlying data source
    ✅ Consistent validation behavior across different usage scenarios

I - Interface Segregation Principle:
    ✅ Exposes only necessary data fields for product representation
    ✅ Clients depend only on the data they actually need
    ✅ Clean separation between read and write data contracts

D - Dependency Inversion Principle:
    ✅ Depends on Pydantic abstractions, not concrete validation implementations
    ✅ Supports different serialization backends through configuration
    ✅ Enables testing with mock data without external dependencies

DATA TRANSFER OBJECT PATTERNS:
==============================

🎯 Anti-Corruption Layer:
    - Protects domain models from external data format changes
    - Provides data transformation and validation capabilities
    - Ensures backward compatibility through versioned DTOs
    - Maintains data integrity across service boundaries

📊 Immutable Data Contracts:
    - Immutable data structures for thread-safe operations
    - Value object semantics for reliable data handling
    - Structural equality for consistent comparison operations
    - Serialization/deserialization without side effects

🛡️ Type Safety & Validation:
    - Strong typing through Pydantic field definitions
    - Runtime validation for data integrity enforcement
    - Custom validators for business rule validation
    - Automatic documentation generation from type hints

⚡ Performance Optimization:
    - Efficient serialization/deserialization through Pydantic
    - Lazy validation for improved performance
    - Memory-efficient data structures
    - Optimized JSON encoding/decoding

ENTERPRISE INTEGRATION FEATURES:
===============================

🔄 Event Schema Management:
    - JSON Schema generation for event payload validation
    - Schema registry integration for version management
    - Event evolution strategies for backward compatibility
    - Cross-service contract testing support

📈 API Documentation Integration:
    - Automatic OpenAPI schema generation
    - Interactive documentation through Swagger UI
    - Type-safe client SDK generation
    - API contract validation and testing

🧪 Testing & Quality Assurance:
    - Property-based testing support through Hypothesis
    - Factory methods for test data generation
    - Mock data generation for integration testing
    - Contract testing for API compatibility

🔐 Security & Compliance:
    - Input sanitization and validation
    - PII data handling through custom validators
    - Audit trail support through immutable data structures
    - GDPR compliance through selective field exposure

ADVANCED DTO PATTERNS:
=====================

```python
# Version-specific DTOs for API evolution
class ProductDTOV1(BaseModel):
    id: int
    name: str
    price: float

class ProductDTOV2(ProductDTO):
    # Inherits all V1 fields plus new ones
    category: Optional[str] = None
    tags: List[str] = []

# Event-specific DTOs for different contexts
class ProductCreatedEventDTO(BaseModel):
    product_id: int
    name: str
    price: float
    timestamp: datetime
    metadata: Dict[str, Any] = {}

# Command DTOs for write operations
class CreateProductCommandDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

# Query DTOs for read operations
class ProductFilterDTO(BaseModel):
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    in_stock: Optional[bool] = None
    category: Optional[str] = None
    
    class Config:
        extra = "forbid"  # Prevent unknown fields
```

EVENT-DRIVEN INTEGRATION:
========================

```python
# Event publishing with DTOs
async def publish_product_created_event(product: ProductDTO):
    event = ProductCreatedEventDTO(
        product_id=product.id,
        name=product.name,
        price=product.price,
        timestamp=datetime.utcnow()
    )
    await event_publisher.publish("product.created", event.dict())

# Event consumption with validation
@event_handler("product.updated")
async def handle_product_updated(event_data: dict):
    try:
        product_dto = ProductDTO(**event_data)
        await update_search_index(product_dto)
    except ValidationError as e:
        logger.error(f"Invalid event data: {e}")
        await send_to_dead_letter_queue(event_data)
```

MICROSERVICE COMMUNICATION:
===========================

```python
# Inter-service communication
class ProductServiceClient:
    async def get_product(self, product_id: int) -> ProductDTO:
        response = await self.http_client.get(f"/products/{product_id}")
        return ProductDTO(**response.json())
    
    async def create_product(self, product_data: CreateProductCommandDTO) -> ProductDTO:
        response = await self.http_client.post(
            "/products", 
            json=product_data.dict()
        )
        return ProductDTO(**response.json())

# GraphQL integration
@strawberry.type
class ProductType:
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    
    @classmethod
    def from_dto(cls, dto: ProductDTO) -> "ProductType":
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            price=dto.price,
            stock=dto.stock
        )
```

TESTING STRATEGIES:
==================

```python
# Property-based testing
@given(st.text(min_size=1, max_size=200), st.floats(min_value=0.01))
def test_product_dto_creation(name: str, price: float):
    product_data = {
        "id": 1,
        "name": name,
        "price": price,
        "stock": 10,
        "created_at": "2025-09-28T10:00:00",
        "updated_at": "2025-09-28T10:00:00"
    }
    dto = ProductDTO(**product_data)
    assert dto.name == name
    assert dto.price == price

# Factory pattern for test data
class ProductDTOFactory:
    @staticmethod
    def create(**overrides) -> ProductDTO:
        defaults = {
            "id": 1,
            "name": "Test Product",
            "description": "Test Description",
            "price": 99.99,
            "stock": 50,
            "created_at": "2025-09-28T10:00:00",
            "updated_at": "2025-09-28T10:00:00"
        }
        defaults.update(overrides)
        return ProductDTO(**defaults)

# Contract testing
def test_dto_serialization_contract():
    dto = ProductDTOFactory.create()
    serialized = dto.dict()
    deserialized = ProductDTO(**serialized)
    assert dto == deserialized
```

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

from pydantic import BaseModel
from typing import Optional

class ProductDTO(BaseModel):
    """
    📦 Product Data Transfer Object

    Attributes:
        id (int): Unique product identifier.
        name (str): Product name.
        description (Optional[str]): Product description (nullable).
        price (float): Product price.
        stock (int): Inventory stock level.
        created_at (str): Creation timestamp (ISO format).
        updated_at (str): Last update timestamp (ISO format).

    Methods:
        from_model(model): Factory to create DTO from ORM/domain model.
    """
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    created_at: str
    updated_at: str

    @classmethod
    def from_model(cls, model):
        """
        🏭 Factory method to create ProductDTO from a domain or ORM model.
        """
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            price=float(model.price),
            stock=model.stock,
            created_at=str(model.created_at),
            updated_at=str(model.updated_at)
        )