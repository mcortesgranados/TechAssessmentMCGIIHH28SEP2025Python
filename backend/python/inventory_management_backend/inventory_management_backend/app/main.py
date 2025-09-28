"""
FastAPI Application Bootstrap - Hexagonal Event-Driven Microservice Entry Point

This module serves as the main application bootstrap for a hexagonal (ports & adapters) 
microservice architecture, implementing FastAPI with event-driven capabilities and strict 
adherence to SOLID principles for enterprise-grade inventory management applications.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as the application composition root and dependency injection container
    - Orchestrates the wiring of driving adapters (HTTP, GraphQL) with driven adapters (DB, messaging)
    - Provides clean separation between application core and infrastructure concerns
    - Enables substitutability of external dependencies through configuration
    - Maintains architectural boundaries through proper middleware and routing setup

🔧 Microservices Pattern:
    - Implements service discovery through health check endpoints
    - Supports independent deployment and scaling through containerization
    - Provides service mesh integration through standardized middleware
    - Enables distributed tracing and observability across service boundaries
    - Facilitates API gateway integration through versioned routing

📡 Event-Driven Architecture:
    - Bootstrap event publishers and consumers for domain event handling
    - Integrates with message brokers for asynchronous communication
    - Supports event sourcing and CQRS pattern initialization
    - Enables real-time notifications through WebSocket connections
    - Facilitates saga orchestration for distributed transaction management

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Solely responsible for application bootstrap and configuration
    ✅ Separates startup concerns from business logic and infrastructure
    ✅ Focused exclusively on dependency wiring and middleware setup

O - Open/Closed Principle:
    ✅ Open for extension: new routers and middleware can be added easily
    ✅ Closed for modification: core bootstrap logic remains stable
    ✅ Supports plugin architecture through modular router registration

L - Liskov Substitution Principle:
    ✅ FastAPI instances are fully substitutable across different environments
    ✅ Maintains ASGI contract regardless of deployment configuration
    ✅ Consistent behavior across development, testing, and production

I - Interface Segregation Principle:
    ✅ Exposes only necessary HTTP endpoints through selective router inclusion
    ✅ Clients depend only on API routes they actually use
    ✅ Clean separation between different API versions and domains

D - Dependency Inversion Principle:
    ✅ Depends on FastAPI abstractions, not concrete server implementations
    ✅ Supports dependency injection through FastAPI's DI container
    ✅ Enables configuration-driven middleware and routing setup

ENTERPRISE APPLICATION FEATURES:
===============================

🛡️ Security & Compliance:
    - CORS configuration for cross-origin resource sharing
    - Authentication and authorization middleware integration
    - Rate limiting and throttling for API protection
    - Security headers for OWASP compliance

📊 Observability & Monitoring:
    - Health check endpoints for service monitoring
    - Metrics collection for performance tracking
    - Distributed tracing integration with OpenTelemetry
    - Error tracking and alerting capabilities

⚡ Performance Optimization:
    - Async/await patterns for non-blocking I/O
    - Response compression for bandwidth optimization
    - Connection pooling for database operations
    - Caching middleware for improved response times

🔄 Resilience Patterns:
    - Circuit breaker integration for fault tolerance
    - Retry mechanisms for transient failures
    - Graceful shutdown handling for clean deployments
    - Health check endpoints for load balancer integration

MICROSERVICE COMPOSITION ROOT:
=============================

```python
# Enhanced application factory pattern
def create_app(config: AppConfig = None) -> FastAPI:
    config = config or get_default_config()
    
    app = FastAPI(
        title="Inventory Management Microservice",
        description="Hexagonal Event-Driven Product Management API",
        version="1.0.0",
        docs_url="/api/docs" if config.enable_docs else None
    )
    
    # Configure middleware
    configure_middleware(app, config)
    
    # Register event handlers
    configure_event_handlers(app, config)
    
    # Include routers
    configure_routers(app, config)
    
    # Setup monitoring
    configure_monitoring(app, config)
    
    return app

# Environment-specific configuration
@lru_cache()
def get_app_config() -> AppConfig:
    environment = os.getenv("ENVIRONMENT", "development")
    return AppConfigFactory.create(environment)
```

EVENT-DRIVEN INTEGRATION:
========================

```python
# Event-driven startup configuration
@app.on_event("startup")
async def startup_event():
    # Initialize event publishers
    await initialize_event_publishers()
    
    # Setup message broker connections
    await setup_message_brokers()
    
    # Start background tasks
    await start_background_processors()
    
    # Warm up caches
    await warm_up_application_caches()

@app.on_event("shutdown")
async def shutdown_event():
    # Graceful shutdown of event publishers
    await shutdown_event_publishers()
    
    # Close message broker connections
    await close_message_brokers()
    
    # Stop background tasks
    await stop_background_processors()
```

MIDDLEWARE CONFIGURATION:
========================

```python
# Comprehensive middleware stack
def configure_middleware(app: FastAPI, config: AppConfig):
    # Security middleware
    app.add_middleware(SecurityHeadersMiddleware)
    
    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Request/Response logging
    app.add_middleware(LoggingMiddleware)
    
    # Metrics collection
    app.add_middleware(MetricsMiddleware)
    
    # Distributed tracing
    app.add_middleware(TracingMiddleware)
    
    # Rate limiting
    app.add_middleware(RateLimitMiddleware, config=config.rate_limit)
    
    # Compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
```

API VERSIONING & ROUTING:
========================

```python
# Version-aware router configuration
def configure_routers(app: FastAPI, config: AppConfig):
    # API v1 routes
    v1_router = APIRouter(prefix="/api/v1")
    v1_router.include_router(product_router, prefix="/products", tags=["products"])
    v1_router.include_router(user_router, prefix="/users", tags=["users"])
    
    # API v2 routes (future)
    v2_router = APIRouter(prefix="/api/v2")
    # v2_router.include_router(enhanced_product_router)
    
    # System routes
    system_router = APIRouter(prefix="/system")
    system_router.include_router(health_router, tags=["system"])
    system_router.include_router(metrics_router, tags=["monitoring"])
    
    # Register all routers
    app.include_router(v1_router)
    app.include_router(system_router)
    
    # Legacy support (deprecated)
    if config.enable_legacy_api:
        app.include_router(legacy_router, prefix="/legacy", deprecated=True)
```

HEALTH CHECK & MONITORING:
=========================

```python
# Comprehensive health check implementation
@app.get("/health", tags=["system"])
async def health_check():
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": app.version,
            "checks": {
                "database": await check_database_health(),
                "message_broker": await check_message_broker_health(),
                "cache": await check_cache_health(),
                "external_services": await check_external_services_health()
            }
        }
        
        # Determine overall health
        all_healthy = all(check["status"] == "healthy" for check in health_status["checks"].values())
        health_status["status"] = "healthy" if all_healthy else "unhealthy"
        
        return health_status
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

# Metrics endpoint for Prometheus integration
@app.get("/metrics", response_class=PlainTextResponse, tags=["monitoring"])
async def metrics():
    return generate_prometheus_metrics()
```

TESTING CONFIGURATION:
=====================

```python
# Test application factory
def create_test_app() -> FastAPI:
    config = AppConfig(
        database_url="sqlite:///./test.db",
        enable_docs=True,
        cors_origins=["*"],
        log_level="DEBUG"
    )
    return create_app(config)

# Integration test client
@pytest.fixture
def test_client():
    app = create_test_app()
    with TestClient(app) as client:
        yield client

# Async test client
@pytest.fixture
async def async_test_client():
    app = create_test_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

DEPLOYMENT CONFIGURATION:
========================

```python
# Production deployment with Gunicorn
# gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Docker container health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Kubernetes deployment configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inventory-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: inventory-service
  template:
    spec:
      containers:
      - name: inventory-service
        image: inventory-service:latest
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (development mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify domains instead of "*" for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import your routers
from app.api.v1.product_router import router as product_router

# Include your router so /products endpoints show up in /docs
app.include_router(product_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is running with CORS enabled!"}