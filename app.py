# my_flask_app/app.py

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import json
import os

app = Flask(__name__)

# --- MongoDB Connection ---
# Make sure MongoDB is running on your machine.
# Replace 'mongodb://localhost:27017/' with your MongoDB connection string if it's different.
# For production, never hardcode credentials like this. Use environment variables.
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.todo_database  # Your database name
    todos_collection = db.todos  # Your collection name for to-do items
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    client = None # Set client to None if connection fails to prevent errors later

# --- Path for data.json ---
# This ensures Flask can find your data.json file regardless of where the app is run from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'data.json')

# --- Basic Home Route ---
@app.route('/')
def home():
    return "<h1>Welcome to your Flask Project!</h1><p>Navigate to /api or /todo</p>"

# --- /api Route (using data.json) ---
@app.route('/api')
def api_route():
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON from data.json"}), 500

# --- To-Do Application Routes ---

@app.route('/todo')
def todo_page():
    # You might want to fetch and display existing To-Do items here later
    return render_template('todo.html')

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    if request.method == 'POST':
        item_name = request.form.get('itemName')
        item_description = request.form.get('itemDescription')
        item_id = request.form.get('itemId')       # From Task 4
        item_uuid = request.form.get('itemUuid')   # From Task 4
        item_hash = request.form.get('itemHash')   # From Task 4

        if item_name and item_description:
            todo_item = {
                "itemName": item_name,
                "itemDescription": item_description,
                "timestamp": datetime.now().isoformat() # Store as ISO format string
            }

            # Add optional fields if they exist in the form
            if item_id:
                todo_item["itemId"] = item_id
            if item_uuid:
                todo_item["itemUuid"] = item_uuid
            if item_hash:
                todo_item["itemHash"] = item_hash

            if client: # Only attempt to insert if MongoDB connection was successful
                try:
                    todos_collection.insert_one(todo_item)
                    return jsonify({"message": "To-Do item added successfully!", "data": todo_item}), 200
                except Exception as e:
                    return jsonify({"error": f"Failed to save to database: {e}"}), 500
            else:
                return jsonify({"error": "Database connection not established. To-Do item not saved."}), 503
        else:
            return jsonify({"error": "Item Name and Item Description are required."}), 400
    return jsonify({"error": "Method Not Allowed"}), 405

# --- Run the Flask App ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True is good for development, disable in production