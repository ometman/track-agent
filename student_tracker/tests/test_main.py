from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from student_tracker.app.main import app
from student_tracker.app.database import Base
from student_tracker.app.api.api import get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_parent():
    response = client.post(
        "/parents/",
        json={"name": "Test Parent", "phone_number": "1234567890"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Parent"
    assert response.json()["phone_number"] == "1234567890"

def test_create_student():
    parent_response = client.post(
        "/parents/",
        json={"name": "Test Parent", "phone_number": "1234567890"},
    )
    parent_id = parent_response.json()["id"]
    response = client.post(
        f"/parents/{parent_id}/students/",
        json={"name": "Test Student"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"
    assert response.json()["parent_id"] == parent_id

def test_notify_in_school():
    parent_response = client.post(
        "/parents/",
        json={"name": "Test Parent", "phone_number": "1234567890"},
    )
    parent_id = parent_response.json()["id"]
    student_response = client.post(
        f"/parents/{parent_id}/students/",
        json={"name": "Test Student"},
    )
    student_id = student_response.json()["id"]
    response = client.post(f"/notify/in-school/{student_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Notification sent successfully"}
