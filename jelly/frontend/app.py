'''
Objective: Build a Flask application with a JSON API route and a frontend form that \
    stores submitted data in MongoDB Atlas, with proper success and error handling.
Task 1: JSON API Route
    1. Create a Flask application with an /api route. When this route is accessed, it should return a JSON list.\
          The data should be stored in a backend file, read from it, and sent as a response.
'''
from flask import Flask, render_template   


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')   

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission and store data in MongoDB Atlas
    # Implement success and error handling here
    return "Form submitted successfully!"  # Placeholder response

if __name__ == '__main__':
    app.run(debug=True, port=8000)  # Running on port 8000 for the frontend

