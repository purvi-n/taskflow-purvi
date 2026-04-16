import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.db.session import get_db
from app.main import app
import asyncpg
from sqlalchemy.pool import NullPool

TEST_DATABASE_URL = "postgresql+asyncpg://purvii@localhost:5432/taskflow_test"
DIRECT_DATABASE_URL = "postgresql://purvii@localhost:5432/taskflow_test"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture(autouse=True)
async def clean_db():
    conn = await asyncpg.connect(DIRECT_DATABASE_URL)
    await conn.execute("TRUNCATE tasks, projects, users CASCADE;")
    await conn.close()

@pytest.fixture(scope="function")
async def client():
    async def _get_test_db():
        async with TestingSessionLocal() as session:
            yield session
        
    app.dependency_overrides[get_db] = _get_test_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
