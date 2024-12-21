from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, medical_history) VALUES (%s, %s, %s) RETURNING id",
        (data['name'], data['age'], data['medical_history'])
    )
    patient_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Patient added successfully", "patient_id": patient_id}), 201

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
