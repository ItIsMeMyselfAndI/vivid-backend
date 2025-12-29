from datetime import datetime
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

    def test_get_history_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        history_id = 20
        response = requests.get(
            f"{self.api_url}/get-settings?user_id={user_id}&history_id={history_id}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_get_histories_from_bot_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        count = 5
        response = requests.get(
            f"{self.api_url}/get-histories-from-bot?user_id={user_id}&count={count}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_create_history_response(self):
        data = CreateHistory(
            page="/dashboard",
            user_id="864b42da-8553-41bb-a2dd-2b0699845136",
            seconds_spent=0,
            updated_at=datetime.now(),
            created_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-history",
            json=data.model_dump(mode="json")
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_update_history_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        history_id = 6
        data = UpdateHistory(
            page="/simulation",
            seconds_spent=4,
            updated_at=datetime.now(),
        )
        response = requests.put(
            f"{self.api_url}/update-history?user_id={user_id}&history_id={history_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")


if __name__ == '__main__':
    unittest.main()
