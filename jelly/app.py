import os, json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

load_dotenv()

app = Flask(__name__)
secret_key = os.getenv("FLASK_SECRET_KEY")
app.secret_key = secret_key  # Required for flashing messages

# Replace with your MongoDB Atlas connection string
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# Select your database and collection
db = client['flask_form_db']
collection = db['submissions']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api')
def api(): 
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify({"message": "Data loaded successfully:", "data": data})
    except FileNotFoundError:
        return jsonify({"error": "Error: The file 'data.json' does not exist."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error: 'data.json' contains invalid or poorly formatted JSON."}), 400


@app.route('/success')
def success():
    return "Data submitted successfully!"

@app.route('/submit', methods=['POST'])
def submit():
    # Get data from HTML form
    name = request.form.get('name')
    email = request.form.get('email')

    # Prepare document dictionary
    data = {
        "name": name,
        "email": email
    }

    # Insert document into MongoDB Atlas collection or throw error
    try:
        collection.insert_one(data)
    except PyMongoError as e:
        # Flash the specific database error to the user
        flash(f"MongoDB Error: {str(e)}", "error")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "error")
        return redirect(url_for('index'))

    return redirect(url_for('success'))

if __name__ == '__main__':
    app.run(debug=True)
