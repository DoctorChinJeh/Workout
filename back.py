
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM workouts")
    workouts = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(workouts)

@app.route('/api/workouts', methods=['POST'])
def add_workout():
    data = request.json
    if not data or 'exercise' not in data or 'sets' not in data or 'reps' not in data or 'weights' not in data:
        return jsonify({'error': 'Missing required fields (exercise, sets, reps, weights'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
           "INSERT INTO workouts (exercise, sets, reps, weights, workout_date, notes) VALUES (%s, %s, %s , %s, %s, %s)",
            (data['exercise'], data['sets'], data['reps'], data['weights'],data['workout_date'],data.get('notes',None))
        )
        connection.commit()
        workouts_id = cursor.lastrowid
        cursor.close()
        connection.close()

        return jsonify({
             'id': workouts_id,
            'exercise': data['exercise'],
            'sets': data['sets'],
            'reps': data['reps'],
            'weights': data['weights'],
            'workout_date': data['workout_date'],
            'notes': data.get('notes')
        }), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM workouts WHERE id = %s", (id,))
    workout = cursor.fetchone()
    cursor.close()
    connection.close()

    if not workout:
        return jsonify({'error': 'workout not found'}), 404

    return jsonify(workout)

@app.route('/api/workouts/<int:id>', methods=['GET'])
def search_workout(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM workouts WHERE id = %s", (id,))
    workout = cursor.fetchone()
    cursor.close()
    connection.close()

    if not workout:
        return jsonify({'error': 'workout not found'}), 404

    return jsonify(workout)



@app.route('/api/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    workout = request.json
    if not workout:
        return jsonify({'error': 'No data provided'}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        updates = []
        values = []
        if 'exercise' in workout:
            updates.append("exercise = %s")
            values.append(workout['exercise'])
        if 'sets' in workout:
            updates.append("sets = %s")
            values.append(workout['sets'])
        if 'reps' in workout:
            updates.append("reps = %s")
            values.append(workout['reps'])
        if 'weights' in workout:
            updates.append("weights = %s")
            values.append(workout['weights'])
        if ' workout_date' in workout:
            updates.append(" workout_date = %s")
            values.append(workout[' workout_date'])
        if 'notes' in workout:
            updates.append("notes = %s")
            values.append(workout['notes'])


        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400

        query = f"UPDATE workouts SET {', '.join(updates)} WHERE id = %s"
        values.append(id)
        cursor.execute(query, tuple(values))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Workouts not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Workouts updated successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM workouts WHERE id = %s", (id,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Workouts not found'}), 404

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Workouts deleted successfully'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
