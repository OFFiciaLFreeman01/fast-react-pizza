import os

# Env vars must be set before anything under app/ is imported, since
# app.config.Settings reads them once at import time.
os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://pizza:pizza@localhost:5432/pizza_test"
)
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("ADMIN_USERNAME", "admin")

import pytest  # noqa: E402
from passlib.context import CryptContext  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

ADMIN_TEST_PASSWORD = "test-admin-pass"
_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
os.environ["ADMIN_PASSWORD_HASH"] = _pwd.hash(ADMIN_TEST_PASSWORD)

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.pizza import Pizza  # noqa: E402

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_pizza(db_session):
    pizza = Pizza(
        name="Margherita",
        ingredients="tomato,mozzarella,basil",
        unit_price=12.00,
        image_url="/images/margherita.jpg",
        sold_out=False,
    )
    db_session.add(pizza)
    db_session.commit()
    db_session.refresh(pizza)
    return pizza


@pytest.fixture
def sold_out_pizza(db_session):
    pizza = Pizza(
        name="Truffle Mushroom",
        ingredients="mozzarella,mushroom,truffle",
        unit_price=17.00,
        image_url="/images/truffle.jpg",
        sold_out=True,
    )
    db_session.add(pizza)
    db_session.commit()
    db_session.refresh(pizza)
    return pizza


@pytest.fixture
def admin_token(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": ADMIN_TEST_PASSWORD},
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]
