import os
import sqlite3 as sl
import scr.navigation_apps.navigations
import datetime
import scr.BD.bd_users.local.update_bd
import scr.BD.bd_users.bd_server_user
import scr.func
import scr.toggle_user_sessions


async def insert_bd_user(id_user, login, password, privileges, first_name, last_name, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, '{login}', '{password}', 
            {privileges}, '{first_name}','{last_name}' ) """
        cursor.execute(query)
    scr.BD.bd_users.bd_server_user.select_task_data_for_update()
    await scr.toggle_user_sessions.handle_user_sessions(page)


def insert_photo(name_file, value, task_id, meter_id=None):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """INSERT INTO picture 
                   (name_file, value, task_id, meter_id) 
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (name_file, value, task_id, meter_id))
        db.commit()
        return cursor.lastrowid


def insert_photo_temp(name_file, value, task_id, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """INSERT INTO picture_temp 
                   (name_file, value, task_id, meter_id) 
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (name_file, value, task_id, meter_id))
        db.commit()


def insert_new_meters(id_task, meter_id, meter_marka, meter_reading, meter_protection, seal_id, remark, meter_type,
                      seal_type):
    """ seal_type здесь заготовка на будующее обновновление сервера"""
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        today_task_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = db.cursor()

        query = """ insert into meters (
                        meter_number, seal_number, type_service, marka_name, antimagnetic_protection, status_filling
                    ) 
                    values (?, ?, ?, ?, ?, ?) """
        cursor.execute(query, (meter_id, seal_id, meter_type, meter_marka, meter_protection, 'выполнен'))
        db.commit()

        query = """ insert into meter_reading (
                        meter_id, last_reading_date, last_reading_value, new_reading_date, new_reading_value
                    )
                    values (?, ?, ?, ?, ?) """
        cursor.execute(query, (meter_id, today, meter_reading, today, meter_reading))
        db.commit()

        query = """ insert into meter_task (meter_id, task_id, remark_meter)
                    values (?,?,?)"""
        cursor.execute(query, (meter_id, id_task, remark))
        db.commit()

        query = f""" update tasks set 
                                   unloading_time = '{str(today)}',  
                                   status = CASE 
                                        WHEN status = 'просрочен' THEN status 
                                        ELSE 'в исполнении' 
                                   END,
                                   unloaded = false
                                   where id = {id_task}"""
        cursor.execute(query)
        db.commit()

        query = f""" insert into picture (value, name_file, task_id, meter_id)
                     select value, name_file, task_id, meter_id from picture_temp
                        """
        cursor.execute(query)
        delete_photo = f""" DROP TABLE picture_temp """
        cursor.execute(delete_photo)
        db.commit()
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(id_task if isinstance(id_task, list) else [id_task])


def insert_acts(id_task, string):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query = f""" INSERT INTO acts 
                     (task_id, date, reason) 
                     VALUES ({id_task}, '{today}', '{string}')"""
        cursor.execute(query)
        db.commit()
        query = f""" update tasks set status = 'в исполнении'
                            where id = {id_task} and status != 'выполнен' """
        cursor.execute(query)
        db.commit()
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(id_task if isinstance(id_task, list) else [id_task])


def insert_deleted_photo(server_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" INSERT INTO delete_picture (server_id) 
                     VALUES ({server_id})"""
        cursor.execute(query)
        db.commit()
