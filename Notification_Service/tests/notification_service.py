import requests
import unittest
 
class TestNotificationService(unittest.TestCase):
    BASE_URL = "http://notification-service:5003/notify"
 
    def test_send_notification(self):
        payload = {
            "patient_id": 1,
            "message": "Your appointment is confirmed for tomorrow at 10 AM."
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["message"], "Notification sent successfully.")
 
    def test_invalid_notification(self):
        payload = {
            "patient_id": "invalid",
            "message": "This should fail."
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 400)
 
if __name__ == "__main__":
    unittest.main()