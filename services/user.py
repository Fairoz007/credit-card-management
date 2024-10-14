
import bcrypt
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId

def register_user(mongo):
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    user_collection = mongo.db.users

    if user_collection.find_one({"email": email}):
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_collection.insert_one({"email": email, "password": hashed_password})

    return jsonify({"msg": "Registration successful"}), 200

def login_user(mongo):
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user_collection = mongo.db.users
    user = user_collection.find_one({"email": email})

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({"access_token": access_token}), 200
