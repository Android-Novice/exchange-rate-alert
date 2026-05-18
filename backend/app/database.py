import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Support Render PostgreSQL (DATABASE_URL) or local SQLite
DATABASE_URL = os.environ.get("DATABASE_URL", "")

if DATABASE_URL:
    # Render provides postgres://, SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
else:
    from pathlib import Path
    DB_PATH = Path(__file__).parent.parent / "exchange_rate.db"
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
