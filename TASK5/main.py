from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

users = {}       # username: hashed_password
tasks = {}       # username: [task1, task2, ...]

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    users[username] = generate_password_hash(password)
    tasks[username] = []
    return jsonify({"message": "Registration successful"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and check_password_hash(users[username], password):
        return jsonify({"message": "Login successful", "user": username}), 200
    return jsonify({"error": "Invalid username or password"}), 401

@app.route('/tasks/<username>', methods=['GET'])
def get_tasks(username):
    if username not in tasks:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"tasks": tasks[username]})

@app.route('/tasks/<username>', methods=['POST'])
def add_task(username):
    data = request.json
    title = data.get("title")
    description = data.get("description")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = {"title": title, "description": description or ""}
    
    if username in tasks:
        tasks[username].append(new_task)
        return jsonify({"message": "Task added successfully"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
