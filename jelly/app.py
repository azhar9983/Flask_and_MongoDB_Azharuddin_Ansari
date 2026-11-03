'''
Objective: Build a Flask application with a JSON API route and a frontend form that \
    stores submitted data in MongoDB Atlas, with proper success and error handling.
Task 1: JSON API Route
    1. Create a Flask application with an /api route. When this route is accessed, it should return a JSON list.\
          The data should be stored in a backend file, read from it, and sent as a response.
'''
from flask import Flask, jsonify


app = Flask(__name__)

# Sample data (in a real application, this would be replaced with actual data from MongoDB)
data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

@app.route('/api', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/')
def index():
    return "Welcome to the Flask JSON API!" 

if __name__ == '__main__':
    app.run(debug=True)

