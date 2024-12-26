import requests
import unittest
 
class TestDataAggregatorService(unittest.TestCase):
    BASE_URL = "http://data-aggregator-service:5004/aggregate"
 
    def test_aggregate_data(self):
        payload = {
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("aggregated_data", response.json())
 
    def test_invalid_date_range(self):
        payload = {
            "start_date": "invalid-date",
            "end_date": "2024-12-31"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 400)
 
    def test_get_aggregated_data(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
 
if __name__ == "__main__":
    unittest.main()