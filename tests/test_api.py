import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_valid_expense(client):
    response = client.post(
        "/finance_tracker",
       json={
           "amount" : 100,
           "type" : "invalid_type",
           "category" : "salary" 
        }
    )

    assert response.status_code == 400

def test_missing_amount_fails(client):
    response = client.post("/finance_tracker",
        json={
            "type" : "expense",
            "category" : "food"
        }
    )

    assert response.status_code == 400
    assert "error" in response.get_json()

def test_invalid_type_fails(client):
    response = client.post("/finance_tracker",
        json = {
            "amount" : 500,
            "type" : "invalid_type",
            "category" : "salary"
        }
    )

    assert response.status_code == 400

def test_get_transactions_returns_list(client):
    response = client.get("/finance_tracker")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

