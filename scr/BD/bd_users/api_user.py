from typing import Dict, List, Any, Optional
from scr.API.api_client import WaterUtilityAPIClient
from dotenv import load_dotenv
import os

# Загрузить переменные окружения из .env
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")


def create_api_client(login: str, password: str) -> WaterUtilityAPIClient:
    return WaterUtilityAPIClient(API_BASE_URL, login, password)


def check_user(login: str, password: str) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.login()
    except Exception as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None


def get_meter_task(login: str, password: str, user_id: int) -> Optional[List[Dict[str, Any]]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.get_active_meter_tasks(user_id)
    except Exception as e:
        print(f"Ошибка при получении задач по счетчикам: {e}")
        return None


def get_latest_readings(login: str, password: str, user_id: int) -> Optional[List[Dict[str, Any]]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.get_latest_meter_readings(user_id)
    except Exception as e:
        print(f"Ошибка при получении последних показаний: {e}")
        return None


def get_meters(login: str, password: str, user_id: int) -> Optional[List[Dict[str, Any]]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.get_meters_from_active_tasks(user_id)
    except Exception as e:
        print(f"Ошибка при получении счетчиков: {e}")
        return None


def get_task(login: str, password: str, user_id: int) -> Optional[List[Dict[str, Any]]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.get_task_data_new(user_id)
    except Exception as e:
        print(f"Ошибка при получении задач: {e}")
        return None


def update_dop_data(login: str, password: str, address_id: int, registered: int, area: float,
                    standarts: float, task_id: int, task_remark: str) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.update_address_task_data(
            address_id, registered, area, standarts, task_id, task_remark
        )
    except Exception as e:
        print(f"Ошибка при обновлении дополнительных данных: {e}")
        return None


def update_meter_reading(login: str, password: str, task_id: int, unloading_date: str,
                         to_server: str, task_remark: str, status: str, meter_id: str,
                         last_reading_date: str, last_reading_value: int, meter_remark: str) -> Optional[
    Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.update_task_meter_data(
            task_id, unloading_date, to_server, task_remark, status,
            meter_id, last_reading_date, last_reading_value, meter_remark
        )
    except Exception as e:
        print(f"Ошибка при обновлении показаний счетчика: {e}")
        return None


def update_meter_seal(login: str, password: str, task_id: int, unloading_date: str,
                      to_server: str, task_remark: str, status: str, meter_id: str,
                      seal_id: str, date_installation: str, meter_remark: str) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.update_task_meter_seal(
            task_id, unloading_date, to_server, task_remark, status,
            meter_id, seal_id, date_installation, meter_remark
        )
    except Exception as e:
        print(f"Ошибка при обновлении пломбы счетчика: {e}")
        return None


def batch_update_tasks(login: str, password: str, task_updates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.batch_update_tasks(task_updates)
    except Exception as e:
        print(f"Ошибка при пакетном обновлении задач: {e}")
        return None


def batch_update_address(login: str, password: str, address_updates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        response = api_client.batch_update_address(address_updates)
        print(f"Ответ сервера: {response}")
        return response
    except Exception as e:
        print(f"Ошибка при пакетном обновлении адресов: {e}")
        return None
