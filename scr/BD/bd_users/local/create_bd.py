import sqlite3 as sl


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_user = """ Create table if not exists user
                (id Integer, login Text, password Text, privileges integer, first_name Text, last_name Text) """

        table_address = """ Create table if not exists address(id integer, city text, district text, hamlet Text, 
                street Text, dom text, apartment text, entrance text, registered_residing Text, standarts REAL, 
                area REAL , type_address Text,
                CONSTRAINT address_pk PRIMARY KEY (id))"""

        table_task = """ Create table if not exists tasks(id Integer, id_address integer, phone_number Text, 
                personal_account Text, fio Text, date Text, date_end text, remark_task Text, status Text, 
                unloading_time Text, purpose Text, saldo Text, unloaded bool,
                CONSTRAINT task_pk PRIMARY KEY (id)) """

        table_meters = """ Create table if not exists meters(
                meter_number Text, seal_number text, instalation_date Text, type_service text, 
                marka_id integer, marka_name Text, date_of_death Text, location Text,
                status_filling Text, antimagnetic_protection bool, average_consumption REAL,
                CONSTRAINT meters_pk PRIMARY KEY (meter_number)) """

        table_meter_reading = """ Create table if not exists meter_reading(
                id integer,
                meter_id integer, last_reading_date Text, last_reading_value Text, 
                new_reading_date Text, new_reading_value Text,
                CONSTRAINT meter_reading_pk PRIMARY KEY (id)) """

        table_meter_task = """ Create table if not exists meter_task(
                id integer,
                meter_id text, task_id integer, remark_meter Text,
                CONSTRAINT meter_task_pk PRIMARY KEY (id)) """

        table_picture = """ Create table if not exists picture(id Integer primary key autoincrement, value BLOB,
                name_file Text, task_id Integer, meter_id Text, server_id int) """

        table_delete_photo = """ Create table if not exists delete_picture (server_id int) """

        table_acts = """ Create table if not exists acts (
                id Integer primary key,
                task_id Integer,
                date Text,
                reason Text,
                made bool,
                not_working_meters Text) """

        cursor.execute(table_user)
        cursor.execute(table_meter_task)
        cursor.execute(table_task)
        cursor.execute(table_meters)
        cursor.execute(table_meter_reading)
        cursor.execute(table_picture)
        cursor.execute(table_delete_photo)
        cursor.execute(table_address)
        cursor.execute(table_acts)


def create_temp_photo_table():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_picture = """ Create table if not exists picture_temp (id Integer primary key autoincrement, value BLOB,
                        name_file Text, task_id Integer, meter_id integer) """
        cursor.execute(table_picture)
        db.commit()
