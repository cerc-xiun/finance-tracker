from database import init_db
from finance_services import insert_record, get_transactions, update_record, delete_record
from flask import Flask, request, jsonify
from enum import StrEnum, auto

app = Flask(__name__)

class Transaction_Type(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"

@app.route("/finance_tracker", methods=['POST'])
def insert_record_route():

    data = request.get_json()

    err = list()
    if not data.get("amount"):
            err.append("Amount")
    if not data.get("category"):
            err.append("Category")
    if data.get("type"):
        if data.get("type").strip().lower() not in [Transaction_Type.EXPENSE, Transaction_Type.INCOME]:
                err.append("Invalid Transaction Type (must me 'income' or 'expense')")
    else:
        err.append("Transaction Type")
    if err:
        return jsonify({"error" : f"Missing Fields: {err}"}), 400

    if result := insert_record(
                    valid_types=Transaction_Type,
                    type=data.get("type").strip().lower(),
                    amount=data.get("amount"),
                    category=data.get('category').strip().lower(),
                    logged_at=data.get("logged_at").strip() if data.get("logged_at") else None,
                    description=data.get("description").strip() if data.get("description") else None
                    ):
        
        return jsonify(result), 201

    else:

        return jsonify(result), 422

@app.route("/finance_tracker", methods=['GET'])
def transaction_list_route():
        
        return jsonify(get_transactions(category=request.args.get("category"))), 200

@app.route("/finance_tracker/<int:id>", methods=['PATCH'])
def update_record_route(id):
    data = request.get_json() or {}
    type = data.get("type", "").strip().lower()
    amount = data.get("amount")
    description = data.get("description")
    logged_at = data.get("logged_at")

    if not type:
        return jsonify({"error" : "Missing type (income or expense)"}), 400
        
    if amount is None and description is None and logged_at is None:
        return jsonify({"error" : "There's nothing to be updated in the specified record"}), 400

    if result := update_record(valid_types=Transaction_Type, id=id,type=type, amount=amount, description=description, logged_at=logged_at):
        return jsonify(result), 200
    else:
        return jsonify(result), 422

@app.route("/finance_tracker/<int:id>", methods=['DELETE'])
def delete_record_route(id):
    data = request.get_json() or {}
    type = data.get("type", "").strip().lower()

    if not type:
        return jsonify({"error" : "Missing type (income or expense)"}), 400
    
    if result := delete_record(valid_types=Transaction_Type, id=id, type=type):
        return jsonify(result), 200
    else:
        return jsonify(result), 404

if __name__ == '__main__':
    init_db()
