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

    def test_get_settings_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        response = requests.get(
            f"{self.api_url}/get-settings?user_id={user_id}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_create_settings_response(self):
        data = CreateSettings(
            user_id="864b42da-8553-41bb-a2dd-2b0699845136",
            theme=SettingsTheme.DARK,
            speed=1.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-settings",
            json=data.model_dump(mode="json")
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_update_settings_response(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        data = UpdateSettings(
            theme=SettingsTheme.LIGHT,
            speed=1.25,
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-settings?user_id={user_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")


if __name__ == '__main__':
    unittest.main()
