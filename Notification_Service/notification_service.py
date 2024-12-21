from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def send_notification():
    data = request.json
    patient_id = data.get("patient_id")
    message = data.get("message")
    # Simulate sending notification
    return jsonify({"message": f"Notification sent to patient {patient_id} about {message}"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)
