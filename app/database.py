import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

DATABASE_URL = (
    "postgresql+psycopg2://"
    f"{require('POSTGRES_USER')}:"
    f"{require('POSTGRES_PASSWORD')}@"
    f"{require('POSTGRES_HOST')}:"
    f"{require('POSTGRES_PORT')}/"
    f"{require('POSTGRES_DB')}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()