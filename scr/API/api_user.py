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


async def start_websocket(login: str, password: str, employee_id: int):
    """Запуск WebSocket для получения уведомлений"""
    api_client = create_api_client(login, password)
    await api_client.start_websocket(employee_id)


async def stop_websocket(login: str, password: str):
    api_client = create_api_client(login, password)
    await api_client.stop_websocket()


def change_flag_notification(login: str, password: str, task_ids: List[int]):
    api_client = create_api_client(login, password)
    api_client.change_flag_notification(task_ids)


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


def batch_update_tasks(login: str, password: str, task_updates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.batch_update_tasks(task_updates)
    except Exception as e:
        print(f"Ошибка при пакетном обновлении задач: {e}")
        return None


def batch_photo(login: str, password: str, photo_update: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    api_client = create_api_client(login, password)
    try:
        return api_client.batch_photo(photo_update)
    except Exception as e:
        print(f"Ошибка при пакетной отгрузке фотографий: {e}")
        return None


def delete_photo(login: str, password: str, photo_delete: List[int]):
    api_client = create_api_client(login, password)
    try:
        return api_client.delete_photo(photo_delete)
    except Exception as e:
        print(f"Ошибка при пакетной отгрузке фотографий: {e}")
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
