from datetime import datetime
import unittest
import requests

from schema.settings import CreateSettings, SettingsTheme, UpdateSettings
import os
from dotenv import load_dotenv


class TestSettingsEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_url = os.environ.get("API_URL")
        if not api_url:
            print("[FAIL] PROJECT_URL doesn't exist")
            exit(0)
        self.api_url = api_url
        self.user_id = "25e7429d-b412-4514-b0d2-36a6bd56fc67"

    def test_get_settings_response(self):
        response = requests.get(
            f"{self.api_url}/get-settings?user_id={self.user_id}"
        )
        self.assertEqual(response.status_code,  200)

    def test_create_settings_response(self):
        data = CreateSettings(
            user_id=self.user_id,
            theme=SettingsTheme.DARK,
            speed=1.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-settings",
            json=data.model_dump(mode="json")
        )
        self.assertEqual(response.status_code,  200)

    def test_update_settings_response(self):
        data = UpdateSettings(
            theme=SettingsTheme.LIGHT,
            speed=1.25,
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-settings?user_id={self.user_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        )
        self.assertEqual(response.status_code,  200)


if __name__ == '__main__':
    unittest.main()
