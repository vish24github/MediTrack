from flask import Flask, jsonify
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

@app.route('/aggregated-data', methods=['GET'])
def get_aggregated_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Example aggregation query
        cursor.execute("""
            SELECT doctor_name, COUNT(*) AS appointment_count
            FROM appointments
            GROUP BY doctor_name
        """)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5004)
