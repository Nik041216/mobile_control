import json
import requests
from typing import List, Dict, Any


class WaterUtilityAPIClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def _make_request(self, method: str, endpoint: str,
                      data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        print(url)
        params = params or {}
        params.update({"username": self.username, "password": self.password})

        try:
            if method == "GET":
                response = self.session.get(url, params=params)
            elif method == "POST":
                response = self.session.post(url, json=data, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            raise

    def login(self) -> Dict[str, Any]:
        return self._make_request("POST", "login", data={"username": self.username, "password": self.password})

    def assign_tasks(self, task_ids: List[int], employee_id: int) -> Dict[str, Any]:
        data = {"task_ids": task_ids, "employee_id": employee_id}
        return self._make_request("POST", "assign_tasks", data=data)

    def get_active_meter_tasks(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"active_meter_tasks/{employee_id}")

    def get_latest_meter_readings(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"latest_meter_readings/{employee_id}")

    def get_employers_for_assign_tasks(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "employers_for_assign_tasks")

    def get_meters_from_active_tasks(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"meters_from_active_tasks/{employee_id}")

    def get_task_data_all(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "task_data_all")

    def get_task_data_new(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"task_data_new/{employee_id}")

    def get_task_data_unassigned(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "task_data_unassigned")

    def update_address_task_data(self, address_id: int, registered_residing: int,
                                 address_area: float, address_standarts: float,
                                 task_id: int, task_remark: str) -> Dict[str, Any]:
        data = {
            "address_id": address_id,
            "registered_residing": registered_residing,
            "address_area": address_area,
            "address_standarts": address_standarts,
            "task_id": task_id,
            "task_remark": task_remark
        }
        return self._make_request("POST", "update_address_task_data", data=data)

    def update_task_meter_data(self, task_id: int, unloading_time: str,
                               time_to_server: str, remark: str, status: str,
                               meter_id: str, last_reading_date: str,
                               last_reading_value: int, meter_remark: str) -> Dict[str, Any]:
        data = {
            "task_id": task_id,
            "unloading_time": unloading_time,
            "time_to_server": time_to_server,
            "remark": remark,
            "status": status,
            "meter_id": meter_id,
            "last_reading_date": last_reading_date,
            "last_reading_value": last_reading_value,
            "meter_remark": meter_remark
        }
        return self._make_request("POST", "update_task_meter_data", data=data)

    def update_task_meter_seal(self, task_id: int, unloading_time: str,
                               time_to_server: str, remark: str, status: str,
                               meter_id: str, seal_number: str,
                               date_installation: str, meter_seal_remark: str) -> Dict[str, Any]:
        data = {
            "task_id": task_id,
            "unloading_time": unloading_time,
            "time_to_server": time_to_server,
            "remark": remark,
            "status": status,
            "meter_id": meter_id,
            "seal_number": seal_number,
            "date_installation": date_installation,
            "meter_seal_remark": meter_seal_remark
        }
        return self._make_request("POST", "update_task_meter_seal", data=data)

    def batch_update_tasks(self, task_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"tasks": task_updates}
        return self._make_request("POST", "batch_update_tasks", data=data)

    def batch_update_address(self, address_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"tasks": address_updates}  # Изменено здесь
        return self._make_request("POST", "batch_update_address", data=data)
