import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace with your MongoDB Atlas connection string
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

# Select your database and collection
db = client['flask_form_db']
collection = db['submissions']

@app.route('/')
def home():
    return render_template('index.html')

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

    # Insert document into MongoDB Atlas collection
    collection.insert_one(data)

    return f"<h3>Thank you, {name}! Your data has been stored in MongoDB Atlas.</h3><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
