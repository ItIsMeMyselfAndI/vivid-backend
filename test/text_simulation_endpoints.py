from datetime import datetime
import unittest
import requests

from schema.simulation import CreateSimulation, SimulationStatus, SimulationType, UpdateSimulation
import os
from dotenv import load_dotenv


class TestSimulationEndpoints(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        api_url = os.environ.get("API_URL")
        if not api_url:
            print("[Exit] PROJECT_URL doesn't exist")
            exit(0)
        self.api_url = api_url

    def test_get_simulation_respond_data(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        simulation_type = SimulationType.STACK.value
        response = requests.get(
            f"{self.api_url}/get-simulation?user_id={user_id}&simulation_type={simulation_type}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_get_all_simulations_respond_data(self):
        user_id = "ee74dbf9-2dc2-491a-a2fa-141e229d74a7"
        response = requests.get(
            f"{self.api_url}/get-all-simulations?user_id={user_id}"
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_create_simulation_respond_data(self):
        data = CreateSimulation(
            type=SimulationType.STACK,
            user_id="864b42da-8553-41bb-a2dd-2b0699845136",
            status=SimulationStatus.NOT_VISITED,
            total_visits=1,
            last_visit_at=datetime.now(),
            seconds_spent=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        response = requests.post(
            f"{self.api_url}/create-simulation",
            json=data.model_dump(mode="json")
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")

    def test_update_simulation_respond_data(self):
        user_id = "864b42da-8553-41bb-a2dd-2b0699845136"
        simulation_type = SimulationType.STACK.value
        data = UpdateSimulation(
            status=SimulationStatus.IN_PROGRESS,
            total_visits=2,
            last_visit_at=datetime.now(),
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-simulation?user_id={user_id}&simulation_type={simulation_type}",
            json=data.model_dump(mode="json", exclude_none=True)
        ).json()
        try:
            print("[INFO]", response["data"])
        except Exception as e:
            self.fail(f"[FAIL] data doesn't exist on the response: {e}")


if __name__ == '__main__':
    unittest.main()
