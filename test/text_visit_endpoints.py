from datetime import datetime
import unittest
import requests

from schema.visit import CreateVisit, UpdateVisit
import os
from dotenv import load_dotenv


class TestVisitEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_url = os.environ.get("API_URL")
        if not api_url:
            print("[FAIL] PROJECT_URL doesn't exist")
            exit(0)
        self.api_url = api_url

    def test_get_visits_respond_data(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        count = 5
        response = requests.get(
            f"{self.api_url}/get-visits?user_id={user_id}&count={count}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_create_visit_respond_data(self):
        data = CreateVisit(
            page="/dashboard",
            user_id="864b42da-8553-41bb-a2dd-2b0699845136",
            opened_at=datetime.now()
        )
        response = requests.post(
            f"{self.api_url}/create-visit",
            json=data.model_dump(mode="json")
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_update_visit_respond_data(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        visit_id = 6
        data = UpdateVisit(
            page="/simulation",
            closed_at=datetime.now(),
        )
        response = requests.put(
            f"{self.api_url}/update-visit?user_id={user_id}&visit_id={visit_id}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")


if __name__ == '__main__':
    unittest.main()
