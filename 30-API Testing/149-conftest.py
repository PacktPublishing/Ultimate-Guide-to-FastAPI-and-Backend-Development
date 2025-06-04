import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.database.session import get_session
from app.main import app
from app.tests import example

# Test database
engine = create_async_engine(url="sqlite+aiosqlite:///:memory:")
test_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False,
)

async def get_session_override():
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def seller_token(client: AsyncClient):
    response = await client.post(
        "/seller/token",
        data={
            "grant_type": "password",
            "username": example.SELLER["email"],
            "password": example.SELLER["password"],
        }
    )
    assert "access_token" in response.json()
    return response.json()["access_token"]


# Can also create a client with the default authorization header
@pytest_asyncio.fixture(scope="session")
async def client_with_auth(client: AsyncClient, seller_token: str):
    # Add the default authorization header
    client.headers["Authorization"] = f"Bearer {seller_token}"
    return client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_and_teardown():
    
    print("🧪 starting tests...")

    app.dependency_overrides[get_session] = get_session_override

    async with engine.begin() as connection:
        from app.database.models import DeliveryPartner, Seller, Shipment  # noqa: F401
        await connection.run_sync(SQLModel.metadata.create_all)

    async with test_session() as session:
        await example.create_test_data(session)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.drop_all)
    
    app.dependency_overrides.clear()

    print("✅ finished!")