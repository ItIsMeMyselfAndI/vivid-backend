from datetime import datetime
import json
import unittest
import requests

from schema.history import CreateHistory, UpdateHistory
import os
from dotenv import load_dotenv


class TestHistoryEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_url = os.environ.get("API_URL")
        if not api_url:
            print("[FAIL] PROJECT_URL doesn't exist")
            exit(0)
        self.api_url = api_url
        self.history_id = 389
        self.user_id = "25e7429d-b412-4514-b0d2-36a6bd56fc67"

    def test_get_history_response(self):
        response = requests.get(
            f"{self.api_url}/get-history?user_id={self.user_id}&history_id={self.history_id}"
        )
        self.assertEqual(response.status_code,  200)

    def test_get_histories_from_bot_response(self):
        limit = 5
        cursor = 1690
        response = requests.get(
            f"{self.api_url}/get-histories-from-bot?user_id={
                self.user_id
            }&cursor={cursor}&limit={limit}"
        )
        print(response.json())
        self.assertEqual(response.status_code,  200)

    def test_create_history_response(self):
        data = CreateHistory(
            page="/dashboard",
            user_id=self.user_id,
            seconds_spent=0,
            updated_at=datetime.now(),
            created_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-history",
            json=data.model_dump(mode="json")
        )
        self.assertEqual(response.status_code,  200)

    def test_update_history_response(self):
        data = UpdateHistory(
            page="/simulation",
            seconds_spent=4,
            updated_at=datetime.now(),
        )
        response = requests.put(
            f"{self.api_url}/update-history?user_id={self.user_id}&history_id={self.history_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        )
        self.assertEqual(response.status_code,  200)

    def test_update_history_time_spent_response(self):
        payload = {
            "authorization": "asdflkjsdlfjslkfjsdj",
            "elapsed_secs": 10,
            "updated_at": "2024-06-10T12:00:00Z"
        }
        response = requests.post(
            f"{self.api_url}/update-history-time-spent?user_id={
                self.user_id}&history_id={self.history_id}",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code,  200)


if __name__ == '__main__':
    unittest.main()
