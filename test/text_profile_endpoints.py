from datetime import datetime
import unittest
import requests

from schema.profile import CreateProfile, UpdateProfile
import os
from dotenv import load_dotenv


class TestProfileEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_url = os.environ.get("API_URL")
        if not api_url:
            print("[FAIL] PROJECT_URL doesn't exist")
            exit(0)
        self.api_url = api_url
        self.user_id = "9ac1cda9-b9b2-4915-9e05-53c44b192b2c"

    def test_get_profile_respond_data(self):
        response = requests.get(
            f"{self.api_url}/get-profile?user_id={self.user_id}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_create_profile_respond_data(self):
        data = CreateProfile(
            id=self.user_id,
            username="sample",
            email="sample@gmail.com",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-profile",
            json=data.model_dump(mode="json")
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_update_profile_respond_data(self):
        data = UpdateProfile(
            username="ger",
            email="egermirasol2023@gmail.com",
            msg_of_the_day="hello world",
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-profile?user_id={self.user_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")


if __name__ == '__main__':
    unittest.main()
