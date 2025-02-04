import json

import datetime
from typing import List, Dict, Any

import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.create_bd
import scr.BD.bd_users.local.update_bd
import scr.func
import scr.navigation_apps.navigations
import scr.BD.bd_users.api_user as api


def select_task_data(id_user):
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record

    task_data = api.get_task(login, password, id_user)
    if task_data:
        for record in task_data:
            scr.BD.bd_users.local.update_bd.update_tasks_data_from_server(
                record['task_id'], record['customer_name'], record['address_id'], record['city'], record['district'],
                record['hamlet'], record['street'], record['house'], record['apartment'], record['entrance'],
                record['phone_number'], record['personal_account'], record['task_date'], record['date_end'],
                record['remark'], record['task_status'], record['purpose'], record['registered_residing'],
                record['standards'], record['area'], record['saldo'], record['type_address']
            )

    meter_task_data = api.get_meter_task(login, password, id_user)
    if meter_task_data:
        for record in meter_task_data:
            scr.BD.bd_users.local.insert_bd.insert_bd_meter_task(
                record['id'], record['task_id'], record['meter_id'], record['meter_remark']
            )

    meter_data = api.get_meters(login, password, id_user)
    if meter_data:
        for record in meter_data:
            scr.BD.bd_users.local.insert_bd.insert_bd_meters(
                record['meter_number'], record['installation_date'], record['type_service'], record['marka_id'],
                record['marka_name'], record['seal_number'], record['date_next_verification'],
                record['location'], record['antimagnetic_protection'],  record['average_consumption']
            )

    meter_reading_data = api.get_latest_readings(login, password, id_user)
    if meter_reading_data:
        for record in meter_reading_data:
            scr.BD.bd_users.local.insert_bd.insert_bd_meter_reading(
                record['id'], record['meter_id'], record['reading_date'], record['reading_value']
            )


def select_task_data_for_update(page):
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record

    task_data = api.get_task(login, password, user_id)
    if task_data:
        for record in task_data:
            scr.BD.bd_users.local.update_bd.update_tasks_data_from_server(
                record['task_id'], record['customer_name'], record['address_id'], record['city'], record['district'],
                record['hamlet'], record['street'], record['house'], record['apartment'], record['entrance'],
                record['phone_number'], record['personal_account'], record['task_date'], record['date_end'],
                record['remark'], record['task_status'], record['purpose'], record['registered_residing'],
                record['standards'], record['area'], record['saldo'], record['type_address']
            )

    meter_task_data = api.get_meter_task(login, password, user_id)
    if meter_task_data:
        for record in meter_task_data:
            scr.BD.bd_users.local.update_bd.update_meter_task_from_server(
                record['id'], record['task_id'], record['meter_id'], record['meter_remark']
            )

    meter_data = api.get_meters(login, password, user_id)
    if meter_data:
        for record in meter_data:
            scr.BD.bd_users.local.update_bd.update_meter_data_from_server(
                record['meter_number'], record['installation_date'], record['type_service'], record['marka_id'],
                record['marka_name'], record['seal_number'],
                record['date_next_verification'], record['location'], record['antimagnetic_protection'],
                record['average_consumption']
            )

    meter_reading_data = api.get_latest_readings(login, password, user_id)
    if meter_reading_data:
        for record in meter_reading_data:
            scr.BD.bd_users.local.update_bd.update_meter_reading_data_from_server(
                record['id'], record['meter_id'], record['reading_date'], record['reading_value']
            )
    scr.func.show_alert_yn(page, "Данные успешно обновлены")


def upload_task_data(login: str, password: str, task_updates: List[Dict[str, Any]]) -> bool:
    """Отправка данных по задачам"""
    try:
        if task_updates:
            print(f"Отправка данных адресов: {json.dumps(task_updates, indent=2, ensure_ascii=False)}")
            result = api.batch_update_tasks(login, password, task_updates)
            return bool(result)
        return True
    except Exception as ex:
        print(f"Ошибка при отправке данных задач: {ex}")
        return False


def upload_address_data(login: str, password: str, address_updates: List[Dict[str, Any]]) -> bool:
    """Отправка данных по адресам"""
    try:
        if address_updates:
            print(f"Отправка данных адресов: {json.dumps(address_updates, indent=2, ensure_ascii=False)}")
            result = api.batch_update_address(login, password, address_updates)
            print(f"Результат отправки: {result}")
            return bool(result)
        else:
            print("Нет данных адресов для отправки")
            return False
    except Exception as ex:
        print(f"Ошибка при отправке данных адресов: {ex}")
        return False


# выгрузка всех данных
def upload_data_to_server(page):
    try:
        # Получаем данные пользователя
        res = scr.BD.bd_users.local.select_bd.select_user_data()
        if not res:
            raise ValueError("Данные пользователя не найдены")

        user_id, login, password, privileges, first_name, last_name = res[0]
        time_to_server = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Получаем данные для выгрузки задач (может быть пустым)
        task_updates = []
        try:
            result = scr.BD.bd_users.local.select_bd.get_data_to_upload()
            if result:
                for record in result:
                    task_id, unloading_time, last_reading_value, last_reading_date, task_remark, \
                        status, meter_id, meter_remark, purpose, seal_number, meter_marka, \
                        antimagnetic_protection, type_water, id_address = record

                    if status != "выполнен":
                        continue

                    if antimagnetic_protection == 1:
                        antimagnetic_protection = True
                    else:
                        antimagnetic_protection = False

                    update_data = {
                        "task_id": task_id,
                        "unloading_time": unloading_time,
                        "time_to_server": time_to_server,
                        "remark": task_remark or "",
                        "status": status,
                        "meter_id": meter_id,
                        "purpose": purpose,
                        "last_reading_date": last_reading_date or "",
                        "last_reading_value": last_reading_value or "",
                        "meter_remark": meter_remark or "",
                        "seal_number": seal_number,
                        "meter_marka": meter_marka,
                        "antimagnetic_protection": antimagnetic_protection,
                        "type_water": type_water,
                        "id_address": id_address
                    }
                    task_updates.append(update_data)
        except Exception as ex:
            print(f"Ошибка при получении данных задач: {ex}")

        # Получаем данные адресов (обязательно должны быть)
        address_result = scr.BD.bd_users.local.select_bd.get_dop_data_to_upload()
        if not address_result:
            raise ValueError("Не удалось получить данные адресов")

        address_updates = [
            {
                "address_id": item[0],
                "registered_residing": item[1],
                "address_standarts": item[2],
                "address_area": item[3],
                "task_remark": item[4] if item[4] is not None else "",
                "task_id": item[5]
            }
            for item in address_result
        ]

        # Отправляем данные независимо друг от друга
        tasks_success = upload_task_data(login, password, task_updates)
        address_success = upload_address_data(login, password, address_updates)
        if address_success:
            scr.func.show_snack_bar(page, "Данные успешно выгружены на сервер")
        else:
            scr.func.show_snack_bar(page, "Ошибка при выгрузке данных адресов")
    except Exception as ex:
        print(f"Ошибка при выгрузке данных: {ex}")
        scr.func.show_snack_bar(page, f"Ошибка при выгрузке данных: {str(ex)}")
