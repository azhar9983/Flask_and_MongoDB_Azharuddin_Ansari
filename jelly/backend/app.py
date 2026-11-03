import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Allow the frontend development server to call this API from another origin.
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

# Initialize MongoDB Client
# The client maintains a built-in connection pool automatically
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# Select the database and the collection
db = client.get_database("users")  # Uses the DB name specified in your URI
users_collection = db["users"]


# 1. CREATE: Add a user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_user = {"name": data["name"], "email": data["email"]}

    # Insert into MongoDB
    result = users_collection.insert_one(new_user)

    return (
        jsonify({"message": "User created", "id": str(result.inserted_id)}),
        201,
    )


# 2. READ: Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = []
    # Fetch all records from the collection
    for user in users_collection.find():
        users.append(
            {
                "id": str(user["_id"]),  # Convert ObjectId to string for JSON serialization
                "name": user.get("name"),
                "email": user.get("email"),
            }
        )
    return jsonify(users), 200


# 3. UPDATE: Modify a user by ID
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json(silent=True) or {}
    updated_fields = {}

    if "name" in data:
        updated_fields["name"] = data["name"]
    if "email" in data:
        updated_fields["email"] = data["email"]

    if not updated_fields:
        return jsonify({"error": "Nothing to update"}), 400

    result = users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": updated_fields}
    )

    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully"}), 200


# 4. DELETE: Remove a user by ID
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Running on port 5000 for the backend API
