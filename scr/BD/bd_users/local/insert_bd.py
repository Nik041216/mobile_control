import os
import sqlite3 as sl
import scr.navigation_apps.navigations


def insert_bd_user(id_user, login, password, privileges, first_name, last_name, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, '{login}', '{password}', 
            {privileges}, '{first_name}','{last_name}' ) """
        cursor.execute(query)
    scr.BD.bd_users.bd_server_user.select_task_data(id_user)
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


def insert_bd_meters(meter_number, instalation_day, meter_type, marka_id, marka, seal_number, seal_date_instalation,
                     date_next_verification, location, antimagnetic_protection, average_consumption):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meters 
        (meter_number, instalation_date, type_service, status_filling, marka_id, marka_name, seal_id, 
        seal_date_instalation, date_next_verification, location, antimagnetic_protection, average_consumption)
         values ({meter_number}, '{instalation_day}', '{meter_type}', 'невыполнено', '{marka_id}', '{marka}', 
                '{seal_number}', '{seal_date_instalation}', '{date_next_verification}', '{location}', 
                {antimagnetic_protection}, {average_consumption})"""
        cursor.execute(query)


def insert_bd_meter_reading(id_meter_reading, meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meter_reading 
        (id, meter_id, last_reading_date, last_reading_value)
         values ({id_meter_reading}, {meter_id}, '{reading_date}', {reading_values}) """
        cursor.execute(query)


def insert_photo(name_file, value, task_id, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """INSERT INTO picture 
                   (name_file, value, task_id, meter_id) 
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (name_file, value, task_id, meter_id))
        db.commit()
