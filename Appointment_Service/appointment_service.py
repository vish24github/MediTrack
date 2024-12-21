from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
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

@app.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.json
    required_fields = ["patient_id", "doctor_name", "appointment_date"]

    # Validate required fields
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO appointments (patient_id, doctor_name, appointment_date, status)
            VALUES (%s, %s, %s, 'Scheduled')
            RETURNING id
            """,
            (data['patient_id'], data['doctor_name'], data['appointment_date'])
        )
        appointment_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Appointment booked successfully", "appointment_id": appointment_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
        appointment = cursor.fetchone()
        cursor.close()
        conn.close()

        if not appointment:
            return jsonify({"error": "Appointment not found"}), 404

        return jsonify(appointment), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
