"""
🚀 Product Data Generator for MySQL

✨ Features:
- Generates random product records with name, brand, description, and reference.
- Inserts data into the MySQL 'products' table for testing and demonstration.

🔒 Credentials are securely loaded from environment variables.

👩‍💻 Author: Manuela Cortés Granados (manuelacortesgranados@gmail.com)
🔗 https://www.linkedin.com/in/mcortesgranados/
📅 Date: 2025-09-28
"""

import os

# --- MySQL settings ---
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
MYSQL_DB = os.environ.get("MYSQL_DB", "technical_assessment_ihh")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# --- JWT settings ---
SECRET_KEY = os.environ.get("SECRET_KEY", "generate-a-strong-key-for-prod")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))