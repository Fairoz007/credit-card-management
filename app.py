
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import timedelta

app = Flask(__name__)

# Configuration for MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/expense_manager"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

mongo = PyMongo(app)
jwt = JWTManager(app)

# Define your collections (tables)
users_collection = mongo.db.users
expenses_collection = mongo.db.expenses
cards_collection = mongo.db.credit_cards

# User registration route
@app.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400
    
    if users_collection.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 400
    
    users_collection.insert_one({"email": email, "password": password})
    return jsonify({"msg": "Registration successful"}), 200

# Login route
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = users_collection.find_one({"email": email, "password": password})
    if not user:
        return jsonify({"msg": "Bad email or password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=str(user["_id"]))
    return jsonify(access_token=access_token), 200

# Add an expense
@app.route("/expense", methods=["POST"])
@jwt_required()
def add_expense():
    current_user = get_jwt_identity()
    expense = {
        "user_id": ObjectId(current_user),
        "amount": request.json["amount"],
        "category": request.json["category"],
        "date": request.json["date"],
        "payment_method": request.json["payment_method"],
        "description": request.json["description"]
    }
    expenses_collection.insert_one(expense)
    return jsonify({"msg": "Expense added successfully"}), 200

# Fetch all expenses for a user
@app.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()
    expenses = expenses_collection.find({"user_id": ObjectId(current_user)})
    expense_list = [{"amount": e["amount"], "category": e["category"], "date": e["date"], "payment_method": e["payment_method"], "description": e["description"]} for e in expenses]
    return jsonify(expense_list), 200

# Add a credit card
@app.route("/credit_card", methods=["POST"])
@jwt_required()
def add_credit_card():
    current_user = get_jwt_identity()
    card = {
        "user_id": ObjectId(current_user),
        "card_name": request.json["card_name"],
        "balance": request.json["balance"],
        "due_date": request.json["due_date"],
        "min_payment": request.json["min_payment"]
    }
    cards_collection.insert_one(card)
    return jsonify({"msg": "Credit card added successfully"}), 200

# Fetch all credit cards for a user
@app.route("/credit_cards", methods=["GET"])
@jwt_required()
def get_credit_cards():
    current_user = get_jwt_identity()
    cards = cards_collection.find({"user_id": ObjectId(current_user)})
    card_list = [{"card_name": c["card_name"], "balance": c["balance"], "due_date": c["due_date"], "min_payment": c["min_payment"]} for c in cards]
    return jsonify(card_list), 200

# Start the app
if __name__ == '__main__':
    app.run(debug=True)
