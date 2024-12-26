import requests
import unittest
 
class TestAppointmentSchedulingService(unittest.TestCase):
    BASE_URL = "http://appointment-scheduling-service:5002/appointments"
 
    def test_add_appointment(self):
        payload = {
            "patient_id": 1,
            "doctor_name": "Dr. Smith",
            "appointment_date": "2024-12-30",
            "reason": "General Checkup"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("appointment_id", response.json())
 
    def test_get_appointment(self):
        appointment_id = 1
        response = requests.get(f"{self.BASE_URL}/{appointment_id}")
        self.assertIn(response.status_code, [200, 404])
 
    def test_get_all_appointments(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
 
if __name__ == "__main__":
    unittest.main()