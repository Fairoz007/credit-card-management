
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from bson.objectid import ObjectId

def add_credit_card(mongo):
    current_user = get_jwt_identity()
    data = request.json
    card = {
        "user_id": ObjectId(current_user),
        "card_name": data.get('card_name'),
        "balance": data.get('balance'),
        "due_date": data.get('due_date'),
        "min_payment": data.get('min_payment'),
        "alerts": False
    }
    mongo.db.credit_cards.insert_one(card)
    return jsonify({"msg": "Credit card added"}), 200

def get_credit_cards(mongo):
    current_user = get_jwt_identity()
    cards = mongo.db.credit_cards.find({"user_id": ObjectId(current_user)})
    return jsonify([{
        "card_name": c['card_name'], "balance": c['balance'],
        "due_date": c['due_date'], "min_payment": c['min_payment'],
        "alerts": c['alerts']
    } for c in cards]), 200
