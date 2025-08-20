from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

#  Change username, password, host if different in pgAdmin
DATABASE_URL = "postgresql+asyncpg://postgres:indra@localhost/employee"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base model class
Base = declarative_base()
