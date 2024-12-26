import unittest
import requests
 
class TestPatientRecordService(unittest.TestCase):
    BASE_URL = "http://localhost:5001/patients"  # Update with the actual service URL if different
 
    def test_add_patient(self):
        """
        Test the POST /patients endpoint to add a new patient.
        """
        payload = {
            "name": "John Doe",
            "age": 30,
            "medical_history": "None"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 201, "Failed to add a patient")
        self.assertIn("patient_id", response.json(), "Response does not contain patient_id")
 
    def test_get_patient(self):
        """
        Test the GET /patients/<patient_id> endpoint to retrieve a patient by ID.
        """
        # First, add a patient to ensure we have a patient ID to retrieve
        payload = {
            "name": "Jane Doe",
            "age": 25,
            "medical_history": "Asthma"
        }
        post_response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(post_response.status_code, 201, "Failed to add a patient")
 
        patient_id = post_response.json().get("patient_id")
        get_response = requests.get(f"{self.BASE_URL}/{patient_id}")
        self.assertEqual(get_response.status_code, 200, "Failed to retrieve the patient")
        self.assertEqual(get_response.json().get("name"), "Jane Doe", "Patient name mismatch")
        self.assertEqual(get_response.json().get("age"), 25, "Patient age mismatch")
        self.assertEqual(get_response.json().get("medical_history"), "Asthma", "Patient medical history mismatch")
 
    def test_get_nonexistent_patient(self):
        """
        Test the GET /patients/<patient_id> endpoint for a non-existent patient.
        """
        response = requests.get(f"{self.BASE_URL}/99999")  # Assuming 99999 is an invalid ID
        self.assertEqual(response.status_code, 404, "Expected 404 for non-existent patient")
 
if __name__ == '__main__':
    unittest.main()