from flask import Flask, jsonify

app = Flask(__name__)

# Sample data (in a real application, this would be replaced with actual data from MongoDB)
data = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

@app.route('/')
def index():
    return "Welcome to the Flask JSON API!"

@app.route('/api', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=9000)  # Running on port 9000 for the backend API
