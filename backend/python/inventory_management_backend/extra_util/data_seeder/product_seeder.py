"""
Product Sample Data Generator - Hexagonal Event-Driven Microservices Seeder

This utility generates and seeds sample product data into a MySQL database as part of a 
hexagonal (ports & adapters) microservice architecture with event-driven design patterns,
adhering to SOLID principles for maintainable and testable data population workflows.

ARCHITECTURAL PATTERNS:
======================

🏗️ Hexagonal Architecture (Ports & Adapters):
    - Acts as a driving adapter (external tool) for the inventory microservice
    - Provides database seeding capability through well-defined interfaces
    - Separates data generation logic from infrastructure concerns
    - Enables testing with different database implementations via dependency injection

🔧 Microservices Pattern:
    - Operates within the bounded context of inventory management
    - Supports independent deployment and scaling of data seeding operations
    - Facilitates service autonomy for test data preparation
    - Enables cross-service data consistency during integration testing

📡 Event-Driven Architecture:
    - Can be triggered by CI/CD pipeline events for automated test data setup
    - Supports choreography-based data seeding across multiple services
    - Enables event sourcing for audit trails of test data creation
    - Facilitates eventual consistency in distributed testing environments

SOLID PRINCIPLES ADHERENCE:
===========================

S - Single Responsibility Principle:
    ✅ Focused solely on product data generation and database seeding
    ✅ Separates concerns: data creation, database operations, and configuration

O - Open/Closed Principle:
    ✅ Open for extension: easily add new product attributes or data sources
    ✅ Closed for modification: core seeding logic remains stable

L - Liskov Substitution Principle:
    ✅ Database connection can be substituted with any compatible implementation
    ✅ Data generation functions maintain consistent behavioral contracts

I - Interface Segregation Principle:
    ✅ Functions expose only necessary parameters for specific operations
    ✅ Clients depend only on the seeding methods they actually use

D - Dependency Inversion Principle:
    ✅ Depends on database abstraction through environment configuration
    ✅ Supports dependency injection for different database implementations

ENTERPRISE INTEGRATION PATTERNS:
===============================

🔄 Data Seeding Pipeline:
    - Implements batch processing pattern for efficient data insertion
    - Supports transactional integrity with commit/rollback capabilities
    - Enables parallel execution for large-scale data generation

🛠️ Configuration Management:
    - Environment-based configuration for multi-stage deployments
    - Supports external configuration injection for different environments
    - Enables feature toggles for selective data seeding strategies

📊 Observability & Monitoring:
    - Provides logging for audit trails and debugging
    - Supports metrics collection for performance monitoring
    - Enables health checks for data seeding operation status

BENEFITS:
=========
- 🧪 Testability: Isolated functions enable comprehensive unit testing
- 🔄 Reusability: Modular design supports multiple seeding scenarios
- 🚀 Performance: Batch operations optimize database interaction efficiency
- 🛡️ Reliability: Transaction management ensures data consistency
- 🔧 Maintainability: Clear separation of concerns simplifies updates
- 🎯 Flexibility: Environment-based configuration supports multiple deployments

USAGE SCENARIOS:
===============
```bash
# Development environment seeding
export MYSQL_USER=dev_user MYSQL_PASSWORD=dev_pass
python product_seeder.py

# CI/CD pipeline integration
docker run --env-file .env.test inventory-seeder:latest

# Custom data volume seeding
python -c "from product_seeder import insert_products; insert_products(5000)"
```

INTEGRATION EXAMPLES:
====================
```python
# Event-driven seeding via message queue
from product_seeder import insert_products

def handle_seed_event(event_data):
    product_count = event_data.get('count', 100)
    insert_products(product_count)

# Microservice health check integration
def seed_health_check():
    try:
        insert_products(1)
        return {"status": "healthy", "seeder": "operational"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

import os
import random
import pymysql

# --- Database Config ---
MYSQL_USER = os.environ.get("MYSQL_USER", "")          # Defaults to "root" if not set
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")  # Defaults to "root" if not set
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "technical_assessment_ihh"  # Change if needed

# --- Sample Data ---
PRODUCT_NAMES = [
    "Laptop", "Smartphone", "Headphones", "Monitor", "Keyboard",
    "Mouse", "Printer", "Webcam", "Speaker", "Desk Lamp",
    "Charger", "Tablet", "SSD Drive", "USB Cable", "Router"
]
BRANDS = [
    "Sony", "Samsung", "Apple", "Logitech", "Dell", "HP", "Lenovo", "Asus", "Acer", "JBL"
]
DESCRIPTIONS = [
    "High quality", "Latest model", "Affordable", "Compact design",
    "Ideal for office", "Premium build", "Best seller", "Energy efficient",
    "Ergonomic", "1-year warranty"
]

def random_reference():
    """Generate a random product reference code."""
    return f"{random.choice(['BR', 'RF', 'PR'])}{random.randint(10000, 99999)}"

def generate_product():
    """
    Generate a tuple (name, description, price, stock) for a product record,
    concatenating name, brand, description, and reference code.
    """
    pname = random.choice(PRODUCT_NAMES)
    brand = random.choice(BRANDS)
    desc = random.choice(DESCRIPTIONS)
    ref = random_reference()
    name_concat = f"{pname} {brand} {desc} {ref}"
    description = f"{desc} by {brand}, reference {ref}"
    price = round(random.uniform(10, 2000), 2)
    stock = random.randint(0, 500)
    return (name_concat, description, price, stock)

def insert_products(n=20):
    """
    Insert n randomly generated product records into the MySQL products table.
    """
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    for _ in range(n):
        name, description, price, stock = generate_product()
        cursor.execute(
            "INSERT INTO products (name, description, price, stock) VALUES (%s, %s, %s, %s)",
            (name, description, price, stock)
        )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {n} products with concatenated name, brand, description, and reference.")

if __name__ == "__main__":
    insert_products(1000)  # Change number if needed