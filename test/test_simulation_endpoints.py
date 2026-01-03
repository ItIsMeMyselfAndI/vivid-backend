from datetime import datetime
import json
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
        self.user_id = "25e7429d-b412-4514-b0d2-36a6bd56fc67"

    def test_get_simulation_response(self):
        simulation_type = SimulationType.STACK.value
        response = requests.get(
            f"{self.api_url}/get-simulation?user_id={self.user_id}&simulation_type={simulation_type}"
        )
        self.assertEqual(response.status_code,  200)

    def test_get_all_simulations_response(self):
        response = requests.get(
            f"{self.api_url}/get-all-simulations?user_id={self.user_id}"
        )
        self.assertEqual(response.status_code,  200)

    def test_create_simulation_response(self):
        data = CreateSimulation(
            type=SimulationType.STACK,
            user_id=self.user_id,
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
        )
        self.assertEqual(response.status_code,  200)

    def test_update_simulation_response(self):
        simulation_type = SimulationType.STACK.value
        data = UpdateSimulation(
            status=SimulationStatus.IN_PROGRESS,
            total_visits=2,
            last_visit_at=datetime.now(),
            updated_at=datetime.now()
        )
        response = requests.put(
            f"{self.api_url}/update-simulation?user_id={self.user_id}&simulation_type={simulation_type}",
            json=data.model_dump(mode="json", exclude_none=True)
        )
        self.assertEqual(response.status_code,  200)

    def test_update_simulation_time_spent_response(self):
        payload = {
            "authorization": "asdflkjsdlfjslkfjsdj",
            "elapsed_secs": 10,
            "updated_at": "2024-06-10T12:00:00Z"
        }
        response = requests.post(
            f"{self.api_url}/update-simulation-time-spent?user_id={
                self.user_id}&simulation_type={SimulationType.STACK.value}",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code,  200)


if __name__ == '__main__':
    unittest.main()
