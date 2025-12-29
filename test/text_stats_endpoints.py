from datetime import datetime
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

    def test_get_stats_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        response = requests.get(
            f"{self.api_url}/get-stats?user_id={user_id}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_create_stats_response(self):
        data = CreateStats(
            user_id="864b42da-8553-41bb-a2dd-2b0699845136",
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
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_update_stats_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        data = UpdateStats(
            current_streak=9,
            longest_streak=9,
            seconds_spent=10.1,
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-stats?user_id={user_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")


if __name__ == '__main__':
    unittest.main()
