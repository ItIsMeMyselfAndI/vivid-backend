from datetime import datetime
import json
import unittest
import requests

from schema.stats import CreateStats, UpdateStats
import os
from dotenv import load_dotenv


class TestStatsEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_url = os.environ.get("API_URL")
        if not api_url:
            print("[FAIL] PROJECT_URL doesn't exist")
            exit(0)
        self.api_url = api_url
        self.user_id = "9ac1cda9-b9b2-4915-9e05-53c44b192b2c"

    def test_get_stats_response(self):
        response = requests.get(
            f"{self.api_url}/get-stats?user_id={self.user_id}"
        ).json()
        self.assertEqual(response.status_code,  200)

    def test_create_stats_response(self):
        data = CreateStats(
            user_id=self.user_id,
            current_streak=0,
            longest_streak=0,
            seconds_spent=0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-stats",
            json=data.model_dump(mode="json")
        ).json()
        self.assertEqual(response.status_code,  200)

    def test_update_stats_response(self):
        data = UpdateStats(
            current_streak=9,
            longest_streak=9,
            seconds_spent=10.1,
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-stats?user_id={self.user_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        self.assertEqual(response.status_code,  200)

    def test_update_stats_time_spent_response(self):
        payload = {
            "access_token": "asdflkjsdlfjslkfjsdj",
            "elapsed_secs": 10,
            "updated_at": "2024-06-10T12:00:00Z"
        }
        response = requests.post(
            f"{self.api_url}/update-stats-time-spent?user_id={self.user_id}",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code,  200)


if __name__ == '__main__':
    unittest.main()
