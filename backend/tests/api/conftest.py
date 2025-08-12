import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.database import Base, get_db

# Create test database engine
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine, 
    class_=AsyncSession
)

@pytest.fixture
async def db():
    """
    Create a fresh database for each test.
    
    This fixture creates all tables, provides a session,
    and then drops all tables after the test is complete.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestingSessionLocal() as session:
        yield session
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client(db):
    """
    Create a test client with a database session override.
    
    This fixture overrides the database dependency to use the test database.
    """
    # Override dependency
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()