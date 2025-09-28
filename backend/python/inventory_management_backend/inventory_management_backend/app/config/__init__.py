import random
from datetime import datetime, timedelta

PRODUCT_NAMES = [
    "Laptop", "Smartphone", "Headphones", "Monitor", "Keyboard",
    "Mouse", "Printer", "Webcam", "Speaker", "Desk Lamp",
    "Charger", "Tablet", "SSD Drive", "USB Cable", "Router"
]

DESCRIPTIONS = [
    "High quality and reliable.",
    "Latest model with advanced features.",
    "Affordable and durable.",
    "Compact design for easy use.",
    "Ideal for office and home.",
    "Premium build and performance.",
    "Best seller in electronics.",
    "Energy efficient and user friendly.",
    "Ergonomic and stylish.",
    "Comes with a 1-year warranty."
]

def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def generate_product(product_id):
    name = random.choice(PRODUCT_NAMES)
    description = random.choice(DESCRIPTIONS)
    price = round(random.uniform(10, 2000), 2)
    stock = random.randint(0, 500)
    now = datetime.now()
    created_at = random_date(now - timedelta(days=365), now)
    updated_at = random_date(created_at, now)
    return {
        "id": product_id,
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

def generate_products(n=20):
    return [generate_product(i+1) for i in range(n)]

if __name__ == "__main__":
    import json
    products = generate_products(1000)
    print(json.dumps(products, indent=2))