import json
import requests
import websockets
import asyncio
import platform
from typing import List, Dict, Any
import scr.BD.bd_users.bd_server_user as bd_update
import scr.BD.bd_users.local.select_bd as select
import scr.BD.bd_users.local.delete_bd as delete


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
                    result = select.select_task_id()
                    if result:
                        bd_update.unload_task(result)
                    result_new_photo = select.select_photo_id()
                    if result_new_photo:
                        bd_update.unload_photo(result_new_photo)
                        print("Отгрузка фото")
                    result_deleted_photo = select.select_deleted_photo_id()
                    if result_deleted_photo:
                        bd_update.delete_photo(result_deleted_photo)
                        print("Удаление фото")
                    result_act = select.select_act_to_upload()
                    if result_act:
                        bd_update.unload_acts()
                        print("Выгрузка актов")
                    while self.running:
                        message = await websocket.recv()
                        data = json.loads(message)
                        print(f"🔔 Уведомление: {data['message']}")
                        print(f"📋 Назначенные задачи: {data['task_ids']}")
                        if data['message'] == "Вам назначены новые задачи":
                            bd_update.select_task_data_for_update()
                        if data['message'] == "С вас сняли задания":
                            delete.delete_task(data['task_ids'])

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
            elif method == "DELETE":
                response = self.session.delete(url, params=params, json=data)
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

    def get_active_meter_tasks(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"active_meter_tasks/{employee_id}")

    def get_latest_meter_readings(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"latest_meter_readings/{employee_id}")

    def get_meters_from_active_tasks(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"meters_from_active_tasks/{employee_id}")

    def get_task_data_new(self, employee_id: int) -> List[Dict[str, Any]]:
        return self._make_request("GET", f"task_data_new/{employee_id}")

    def batch_update_tasks(self, task_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"tasks": task_updates}
        return self._make_request("POST", "batch_update_tasks", data=data)

    def batch_photo(self, photo_update: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"photos": photo_update}
        return self._make_request("POST", "batch_photo", data=data)

    def batch_act(self, acts_update: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"acts": acts_update}
        return self._make_request("POST", "batch_act", data=data)

    def delete_photo(self, photo_del:List[int]):
        return self._make_request("DELETE", "delete_photo", data=photo_del)

    def batch_update_address(self, address_updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        data = {"tasks": address_updates}  # Изменено здесь
        return self._make_request("POST", "batch_update_address", data=data)
