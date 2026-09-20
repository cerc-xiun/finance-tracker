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
           "amount" : 60.69,
           "type" : "expense",
           "category" : "food",
           "description" : "shawarma boiii" 
        }
    )
    assert response.status_code == 201
    assert "message" in response.get_json()

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

def test_update_record(client):
    response = client.patch("/finance_tracker/1",
        json={
            "type": "expense"
        }
    )
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_delete_missing_type_fails(client):
    response = client.delete("/finance_tracker/1",
        json={}
    )
    assert response.status_code == 400

def test_get_summary_returns_totals(client):
    response = client.get("/finance_tracker/summary")
    assert response.status_code == 200

    data = response.get_json()
    assert "summary" in data
    summary = data["summary"]
    assert "total_income" in summary
    assert "total_expenses" in summary
    assert "net_savings" in summary