import json
import requests
import websockets
import asyncio
import platform
from typing import List, Dict, Any
import scr.BD.bd_users.bd_server_user as bd_update


class WaterUtilityAPIClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.websocket_task = None
        self.running = False
        self.websocket = None  # Добавляем атрибут для хранения WebSocket-соединения

    async def connect_websocket(self, employee_id: int):
        """Асинхронное подключение к WebSocket с переподключением"""
        ws_url = f"ws://{self.base_url.replace('http://', '').replace('https://', '')}/ws/{employee_id}?username={self.username}&password={self.password}"
        self.running = True
        print(f"🔌 Подключение к WebSocket: {ws_url}")

        while self.running:
            try:
                async with websockets.connect(ws_url) as websocket:
                    self.websocket = websocket  # Сохраняем соединение
                    print(f"✅ Подключено к WebSocket для сотрудника {employee_id}")

                    while self.running:
                        message = await websocket.recv()
                        data = json.loads(message)
                        print(f"🔔 Уведомление: {data['message']}")
                        print(f"📋 Назначенные задачи: {data['task_ids']}")
                        if data:
                            bd_update.select_task_data_for_update()

            except websockets.exceptions.ConnectionClosed:
                print("⚠️ Соединение с WebSocket закрыто. Переподключение...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"⚠️ Ошибка WebSocket: {e}")
                await asyncio.sleep(5)

    async def start_websocket(self, employee_id: int):
        """Запуск WebSocket через новый event loop (для ПК и мобильных устройств)"""
        self.websocket_task = asyncio.create_task(self.connect_websocket(employee_id))

    async def stop_websocket(self):
        """Остановка WebSocket"""
        print("Закрываем WebSocket-соединение...")
        self.running = False  # Останавливаем цикл переподключения

        # Закрываем соединение, если оно открыто
        if self.websocket and not self.websocket.closed:
            try:
                await self.websocket.close()
                print("WebSocket соединение закрыто.")
            except Exception as e:
                print(f"Ошибка при закрытии WebSocket: {e}")

        # Отменяем задачу, если она существует
        if self.websocket_task:
            self.websocket_task.cancel()
            try:
                await self.websocket_task  # Ждем завершения задачи
            except asyncio.CancelledError:
                print("WebSocket задача отменена.")
            except Exception as e:
                print(f"Ошибка при отмене задачи: {e}")
            self.websocket_task = None

        print("WebSocket полностью остановлен.")

    def _make_request(self, method: str, endpoint: str,
                      data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
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

    def change_flag_notification(self, task_ids: List[int]):
        return self._make_request("POST", "change_flag_notification", data=task_ids)

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

    def batch_update_tasks(self, task_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"tasks": task_updates}
        return self._make_request("POST", "batch_update_tasks", data=data)

    def batch_update_address(self, address_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"tasks": address_updates}  # Изменено здесь
        return self._make_request("POST", "batch_update_address", data=data)
