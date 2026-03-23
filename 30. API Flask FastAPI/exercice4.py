from flask import Flask, request, jsonify

app = Flask(__name__)

users_db = {
    1: {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "password": "secure123",
        "age": 25,
    }
}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing username, email, or password"}), 400
    
    user_id = len(users_db) + 1
    new_user = {
        "id": user_id,
        "username": data['username'],
        "email": data['email'],
        "password": data['password'],
        "age": data.get('age', None)
    }
    users_db[user_id] = new_user
    return jsonify({"message": "User registered successfully", "user": new_user}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)