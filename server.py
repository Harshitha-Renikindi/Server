from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

# Replace these with your own PostgreSQL connection details
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = '2004'

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST
        )
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

@app.route('/users', methods=['GET'])
def get_users():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(users), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'User added successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET username = %s, password = %s, role = %s WHERE userid = %s", (username, password, role, user_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'User updated successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE userid = %s", (user_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
