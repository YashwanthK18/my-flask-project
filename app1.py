from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient # Import MongoClient

app = Flask(__name__)

# MongoDB Connection (Replace with your actual connection string)
client = MongoClient('mongodb://localhost:27017/') # Adjust if MongoDB is elsewhere
db = client.todo_database # Your database name
todos_collection = db.todos # Your collection name

# ... existing routes ...

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    if request.method == 'POST':
        item_name = request.form.get('itemName')
        item_description = request.form.get('itemDescription')

        if item_name and item_description:
            todo_item = {
                "itemName": item_name,
                "itemDescription": item_description,
                "timestamp": datetime.now() # Don't forget to import datetime
            }
            todos_collection.insert_one(todo_item)
            return jsonify({"message": "To-Do item added successfully!"}), 200
        else:
            return jsonify({"error": "Item Name and Item Description are required."}), 400
    return jsonify({"error": "Method Not Allowed"}), 405

# ... existing app.run() ...