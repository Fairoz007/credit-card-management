
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from bson.objectid import ObjectId

def add_expense(mongo):
    current_user = get_jwt_identity()
    data = request.json
    expense = {
        "user_id": ObjectId(current_user),
        "amount": data.get('amount'),
        "category": data.get('category'),
        "date": data.get('date'),
        "payment_method": data.get('payment_method'),
        "description": data.get('description'),
        "paid": False
    }
    mongo.db.expenses.insert_one(expense)
    return jsonify({"msg": "Expense added successfully"}), 200

def edit_expense(mongo, expense_id):
    current_user = get_jwt_identity()
    data = request.json
    mongo.db.expenses.update_one(
        {"_id": ObjectId(expense_id), "user_id": ObjectId(current_user)},
        {"$set": {
            "amount": data.get('amount'),
            "category": data.get('category'),
            "payment_method": data.get('payment_method'),
            "description": data.get('description'),
            "paid": data.get('paid')
        }}
    )
    return jsonify({"msg": "Expense updated"}), 200

def delete_expense(mongo, expense_id):
    current_user = get_jwt_identity()
    mongo.db.expenses.delete_one({"_id": ObjectId(expense_id), "user_id": ObjectId(current_user)})
    return jsonify({"msg": "Expense deleted"}), 200

def get_expenses(mongo):
    current_user = get_jwt_identity()
    expenses = mongo.db.expenses.find({"user_id": ObjectId(current_user)})
    return jsonify([{
        "amount": e['amount'], "category": e['category'], "date": e['date'],
        "payment_method": e['payment_method'], "description": e['description'],
        "paid": e['paid']
    } for e in expenses]), 200
