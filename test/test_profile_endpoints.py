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
        self.user_id = "25e7429d-b412-4514-b0d2-36a6bd56fc67"

    def test_get_profile_response(self):
        response = requests.get(
            f"{self.api_url}/get-profile?user_id={self.user_id}"
        )
        self.assertEqual(response.status_code,  200)

    # def test_create_profile_response(self):
    #     data = CreateProfile(
    #         id=self.user_id,
    #         username="sample",
    #         email="sample@gmail.com",
    #         created_at=datetime.now(),
    #         updated_at=datetime.now()
    #     )
    #     response = requests.post(
    #         f"{self.api_url}/create-profile",
    #         json=data.model_dump(mode="json")
    #     )
        # self.assertEqual(response.status_code,  200)

    def test_update_profile_response(self):
        data = UpdateProfile(
            username="ger",
            monthly_messages=["hello world", "ldskfslkdjf"],
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-profile?user_id={self.user_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        )
        self.assertEqual(response.status_code,  200)

    def test_generate_profile_monthly_messages(self):
        response = requests.post(
            f"{self.api_url}/generate-profile-monthly-messages",
        )
        self.assertEqual(response.status_code,  200)


if __name__ == '__main__':
    unittest.main()
