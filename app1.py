from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ... existing routes ...

@app.route('/todo')
def todo_page():
    return render_template('todo.html')

# ... existing app.run() ...