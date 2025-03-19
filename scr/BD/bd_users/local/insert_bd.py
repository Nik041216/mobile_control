import os
import sqlite3 as sl
import scr.navigation_apps.navigations
import datetime


def insert_bd_user(id_user, login, password, privileges, first_name, last_name, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, '{login}', '{password}', 
            {privileges}, '{first_name}','{last_name}' ) """
        cursor.execute(query)
    scr.BD.bd_users.bd_server_user.select_task_data_for_update()
    scr.navigation_apps.navigations.role_definition(privileges, page)


def insert_bd_task(task_id, name, address_id, city, district, hamlet, street, dom, apartment,
                   entrance, phone_number, personal_account, date_task, date_end, task_remark, status_task, purpose,
                   registered_residing, standarts, area, saldo, type_address):
    if hamlet is None:
        hamlet = ""
    if street is None:
        street = ""
    if dom is None:
        dom = ""
    if apartment is None:
        apartment = ""
    if entrance is None:
        entrance = ""
    if city is None:
        city = ""
    if district is None:
        district = ""
    if type_address is None:
        type_address = ""
    if task_remark is None:
        task_remark = ""
    if area is None:
        area = 0.0
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into tasks 
        (id, fio, id_address, phone_number, personal_account, date, date_end, remark_task, status, purpose, saldo)
         values ({task_id}, '{name}', {address_id}, '{phone_number}', '{personal_account}', 
            '{date_task}','{date_end}', '{task_remark}', '{status_task}', '{purpose}', {saldo}) """
        cursor.execute(query)

        query2 = f""" Insert into address values ({address_id}, '{city}', '{district}', '{hamlet}', '{street}', '{dom}', 
            '{apartment}', '{entrance}', {registered_residing},  {standarts}, {area}, '{type_address}')"""
        cursor.execute(query2)


def insert_bd_meter_task(meter_task_id, task_id, meter_id, meter_remark):
    if meter_remark is None:
        meter_remark = ""
        with sl.connect('database_client.db') as db:
            cursor = db.cursor()
            query = f""" Insert into meter_task values (
                {meter_task_id}, '{meter_id}', {task_id}, '{meter_remark}')"""
            cursor.execute(query)


def insert_bd_meters(meter_number, instalation_day, meter_type, marka_id, marka, seal_number,
                     date_next_verification, location, antimagnetic_protection, average_consumption):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meters 
        (meter_number, instalation_date, type_service, status_filling, marka_id, marka_name, seal_number, 
        date_of_death, location, antimagnetic_protection, average_consumption)
         values ('{meter_number}', '{instalation_day}', '{meter_type}', 'невыполнено', '{marka_id}', '{marka}', 
                '{seal_number}', '{date_next_verification}', '{location}', 
                {antimagnetic_protection}, {average_consumption})"""
        cursor.execute(query)


def insert_bd_meter_reading(id_meter_reading, meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meter_reading 
        (id, meter_id, last_reading_date, last_reading_value)
         values ({id_meter_reading}, '{meter_id}', '{reading_date}', {reading_values}) """
        cursor.execute(query)


def insert_photo(name_file, value, task_id, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """INSERT INTO picture 
                   (name_file, value, task_id, meter_id) 
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (name_file, value, task_id, meter_id))
        db.commit()


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
                                   status = 'в исполнении'
                                   where id = {id_task}"""
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
                                    unloading_time = '{str(today)}',  
                                    status = 'выполнен'
                                    WHERE id = {id_task} AND id IN (
                                    SELECT DISTINCT t.id
                                    FROM tasks t
                                    JOIN address a ON t.id_address = a.id
                                    JOIN meter_task mt ON t.id = mt.task_id
                                    JOIN meters m ON mt.meter_id = m.meter_number
                                    WHERE NOT EXISTS (
                                        SELECT 1
                                        FROM meters m2
                                        JOIN meter_task mt2 ON m2.meter_number = mt2.meter_id
                                        WHERE m2.meter_number IN (
                                            SELECT meter_id 
                                            FROM meter_task 
                                            WHERE task_id = t.id
                                        )
                                        AND NOT EXISTS (
                                            SELECT 1
                                            FROM meter_reading mr
                                            WHERE mr.meter_id = m2.meter_number
                                            AND mr.new_reading_value IS NOT NULL
                                        )
                                    )
                                );
                          """
        cursor.execute(query)
        db.commit()
        query = f""" insert into picture (value, name_file, task_id, meter_id)
                     select value, name_file, task_id, meter_id from picture_temp
                        """
        cursor.execute(query)
        delete_photo = f""" DROP TABLE picture_temp """
        cursor.execute(delete_photo)
        db.commit()


def insert_acts(id_task, string):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query = f""" INSERT INTO acts 
                     (task_id, date, reason) 
                     VALUES ({id_task}, '{today}', '{string}')"""
        cursor.execute(query)
        db.commit()
