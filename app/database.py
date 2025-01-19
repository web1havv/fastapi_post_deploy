import os
import time

import psycopg2
from psycopg2.extras import RealDictCursor  # type: ignore
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use environment variable for the database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:vaibhav@localhost:5432/fastapi"

# SQLAlchemy engine and session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Psycopg2 connection for raw SQL (optional)
while True:
    try:
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URL, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Unable to connect to the database", error)
        time.sleep(5)
