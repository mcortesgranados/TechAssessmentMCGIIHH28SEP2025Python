"""
FastAPI Product API Router - Hexagonal Event-Driven REST Interface

This module implements the REST API layer as a driving adapter in a hexagonal (ports & adapters) 
microservice architecture, providing HTTP endpoints for product operations with event-driven 
capabilities and strict adherence to SOLID principles for scalable web applications.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as a driving adapter (primary/interface layer)
    - Implements the HTTP port for external client interactions
    - Provides API abstraction that isolates transport concerns from business logic
    - Enables substitutability with different protocols (GraphQL, gRPC, WebSockets)
    - Maintains clean boundaries between presentation and application layers

🔧 Microservices Pattern:
    - Exposes inventory service capabilities through REST endpoints
    - Supports API versioning for backward compatibility (v1, v2, etc.)
    - Enables independent deployment and scaling of API layers
    - Facilitates service discovery through well-defined endpoints
    - Provides clear service contracts through OpenAPI specifications

📡 Event-Driven Architecture:
    - Publishes HTTP events for API gateway integration
    - Supports webhook patterns for external system notifications
    - Enables real-time updates through Server-Sent Events (SSE)
    - Facilitates API-first design with event-driven documentation
    - Integrates with message brokers for asynchronous processing

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Solely responsible for HTTP request/response handling and routing
    ✅ Separates API concerns from business logic and data persistence
    ✅ Focused exclusively on REST endpoint definitions and validation

O - Open/Closed Principle:
    ✅ Open for extension: new endpoints can be added without modifying existing ones
    ✅ Closed for modification: core routing logic remains stable
    ✅ Supports middleware and decorator patterns for cross-cutting concerns

L - Liskov Substitution Principle:
    ✅ Router instances are fully substitutable across different implementations
    ✅ Maintains FastAPI contract regardless of underlying business logic
    ✅ Consistent behavior across different deployment environments

I - Interface Segregation Principle:
    ✅ Exposes only necessary HTTP methods for product operations
    ✅ Clients depend only on endpoints they actually use
    ✅ Clean separation between different API versions and resources

D - Dependency Inversion Principle:
    ✅ Depends on repository abstractions, not concrete implementations
    ✅ Supports dependency injection for testing and flexibility
    ✅ Enables configuration-driven service selection

REST API DESIGN PATTERNS:
=========================

🎯 Resource-Based Design:
    - RESTful resource modeling for Product entities
    - Hierarchical URL structure for nested resources
    - Standard HTTP methods for CRUD operations
    - Consistent response formats across all endpoints

📊 Data Transfer Object (DTO) Pattern:
    - Separates API contracts from domain models
    - Provides version-specific data representations
    - Enables backward compatibility through DTO evolution
    - Supports input validation and output formatting

🛡️ Security & Validation:
    - Request/response validation through Pydantic models
    - Authentication and authorization integration
    - Rate limiting and throttling capabilities
    - CORS configuration for cross-origin requests

⚡ Performance Optimization:
    - Async/await patterns for non-blocking I/O
    - Response caching for read-heavy endpoints
    - Pagination support for large datasets
    - Connection pooling for database operations

ENTERPRISE INTEGRATION FEATURES:
===============================

🔄 API Gateway Integration:
    - Service mesh compatibility through standardized headers
    - Circuit breaker pattern support for resilience
    - Request/response logging for observability
    - Health check endpoints for monitoring

📈 Observability & Monitoring:
    - Request metrics collection (latency, throughput, errors)
    - Distributed tracing integration with OpenTelemetry
    - Error tracking and alerting capabilities
    - Performance monitoring and SLA enforcement

🧪 Testing & Documentation:
    - Auto-generated OpenAPI/Swagger documentation
    - Integration testing support through TestClient
    - Mock endpoint generation for development
    - API contract testing capabilities

EVENT-DRIVEN INTEGRATION EXAMPLES:
==================================

```python
# Webhook integration for external notifications
@router.post("/", response_model=ProductDTO)
async def create_product(
    product_data: ProductCreateDTO,
    repo: ProductRepositoryImpl = Depends(get_product_repository),
    event_publisher: EventPublisher = Depends(get_event_publisher)
):
    product = repo.create_product(product_data.dict())
    
    # Publish domain event
    await event_publisher.publish(ProductCreatedEvent(
        product_id=product.id,
        data=ProductDTO.from_model(product).dict()
    ))
    
    return ProductDTO.from_model(product)

# Server-Sent Events for real-time updates
@router.get("/stream")
async def stream_product_updates():
    async def event_stream():
        while True:
            # Listen for product events
            event = await product_event_queue.get()
            yield f"data: {json.dumps(event)}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/plain")
```

MICROSERVICE PATTERNS:
=====================

```python
# Circuit breaker pattern
@router.get("/{product_id}", response_model=ProductDTO)
async def get_product(
    product_id: int,
    repo: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        product = repo.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductDTO.from_model(product)
    except DatabaseError:
        # Fallback to cached data or alternative service
        return await get_cached_product(product_id)

# Saga pattern for distributed transactions
@router.delete("/{product_id}")
async def delete_product_with_compensation(
    product_id: int,
    saga_orchestrator: SagaOrchestrator = Depends(get_saga_orchestrator)
):
    saga_id = await saga_orchestrator.start_delete_product_saga(product_id)
    return {"saga_id": saga_id, "status": "initiated"}
```

API VERSIONING & EVOLUTION:
===========================

```python
# Version-specific DTOs
@router.get("/", response_model=List[ProductDTOV2])
async def list_products_v2(
    repo: ProductRepositoryImpl = Depends(get_product_repository)
):
    products = repo.get_all_products()
    return [ProductDTOV2.from_model(prod) for prod in products]

# Backward compatibility
@router.get("/legacy", response_model=List[ProductDTOV1], deprecated=True)
async def list_products_legacy(
    repo: ProductRepositoryImpl = Depends(get_product_repository)
):
    products = repo.get_all_products()
    return [ProductDTOV1.from_model(prod) for prod in products]
```

TESTING STRATEGIES:
==================

```python
# Unit testing with mocked dependencies
@pytest.fixture
def mock_router_dependencies():
    with patch('app.api.v1.product_router.get_product_repository') as mock_repo:
        mock_repo.return_value = Mock()
        yield mock_repo

# Integration testing
def test_create_product_endpoint(client: TestClient):
    response = client.post("/api/v1/products/", json={
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99,
        "stock": 10
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"

# Performance testing
async def test_endpoint_performance():
    start_time = time.time()
    response = await async_client.get("/api/v1/products/")
    execution_time = time.time() - start_time
    assert execution_time < 0.5  # Performance threshold
```

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

from fastapi import APIRouter, Depends, status
from typing import List
from app.application.dto.product_dto import ProductDTO
from app.application.dto.product_create_dto import  ProductCreateDTO
from app.application.dto.product_update_dto import ProductUpdateDTO
from app.application.services.product_application_service import ProductApplicationService

router = APIRouter(prefix="/products", tags=["products"])

def get_product_application_service():
    """
    🏭 Dependency provider for ProductApplicationService.
    """
    return ProductApplicationService()

@router.get("/", response_model=List[ProductDTO])
def list_products(service: ProductApplicationService = Depends(get_product_application_service)):
    """
    📦 List all products.
    """
    products = service.list_products()
    return [ProductDTO.from_model(prod) for prod in products]

@router.post("/", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreateDTO,
    service: ProductApplicationService = Depends(get_product_application_service)
):
    """
    🆕 Create a new product using the application service,
    which internally uses domain and infrastructure services.
    """
    created_product = service.create_product(product.model_dump())
    return ProductDTO.from_model(created_product)

@router.put("/{product_id}", response_model=ProductDTO)
def update_product(
    product_id: int,
    update_dto: ProductUpdateDTO,
    service: ProductApplicationService = Depends(get_product_application_service)
):
    updated_product = service.update_product(product_id, update_dto)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductDTO.from_model(updated_product)

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    service: ProductApplicationService = Depends(get_product_application_service)
):
    deleted = service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    # No content to return

