import sqlite3 as sl
import datetime
import scr.BD.bd_users.bd_server_user
import scr.func


def update_local_tasks(unloading_time, task_id, reading_value, remark, meter_id):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query1 = f""" update meter_reading set  
                    new_reading_date = '{today}',
                    new_reading_value = '{reading_value}'
                    where meter_id = '{meter_id}' """
        query2 = f""" update meters set  
                    status_filling = 'выполнен'
                    where meter_number = '{meter_id}' """
        query3 = f""" update meter_task set  
                    remark_meter = '{remark}'
                    where meter_id = '{meter_id}' """
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        db.commit()

        query = f""" update tasks set 
                   unloading_time = '{unloading_time}',  
                   status = 'в исполнении',
                   unloaded = false
                   where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(task_id if isinstance(task_id, list) else [task_id])


def update_not_working_meters(unloading_time, task_id, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update meters set  
                    status_filling = 'выполнен'
                    where meter_number = '{meter_id}' """
        cursor.execute(query)
        db.commit()
        query = f""" update tasks set 
                           unloading_time = '{unloading_time}',  
                           status = 'в исполнении',
                           unloaded = false
                           where id = {task_id}"""
        cursor.execute(query)
        db.commit()


def completed_task(task_id, unloading_time):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
                   unloading_time = '{unloading_time}',  
                   status = 'выполнен',
                   unloaded = false
                   where id = {task_id}"""
        cursor.execute(query)
        db.commit()
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(task_id if isinstance(task_id, list) else [task_id])


def update_remark_task(remark, task_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
            remark_task = '{remark}',
            unloaded = false
            where id = {task_id} """
        cursor.execute(query)
        db.commit()
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(task_id if isinstance(task_id, list) else [task_id])


def update_tasks_data_from_server(task_id, name, address_id, city, district, hamlet, street, dom, apartment,
                                  entrance, phone_number, personal_account, date_task, date_end, task_remark,
                                  status_task, purpose, registered_residing, standarts, area, saldo, type_address):
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

    with sl.connect('database_client.db') as db:
        cursor = db.cursor()

        # Запрос для таблицы tasks
        query_tasks = """
        INSERT INTO tasks (id, fio, id_address, phone_number, personal_account, date, date_end, remark_task, status, purpose, saldo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            fio = excluded.fio,
            id_address = excluded.id_address,
            phone_number = excluded.phone_number,
            personal_account = excluded.personal_account,
            date = excluded.date,
            date_end = excluded.date_end,
            remark_task = excluded.remark_task,
            purpose = excluded.purpose,
            saldo = excluded.saldo
        """
        cursor.execute(query_tasks, (
            task_id, name, address_id, phone_number, personal_account,
            date_task, date_end, task_remark, status_task, purpose, saldo
        ))

        # Запрос для таблицы address
        query_address = """
        INSERT INTO address (id, city, district, hamlet, street, dom, apartment, entrance, registered_residing, 
            standarts, area, type_address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            city = excluded.city,
            district = excluded.district,
            hamlet = excluded.hamlet,
            street = excluded.street,
            dom = excluded.dom,
            apartment = excluded.apartment,
            entrance = excluded.entrance,
            registered_residing = excluded.registered_residing,
            standarts = excluded.standarts,
            area = excluded.area,
            type_address = excluded.type_address
        """
        cursor.execute(query_address, (
            address_id, city, district, hamlet, street, dom, apartment, entrance,
            registered_residing or 0, standarts or 0, area or 0, type_address
        ))

        db.commit()


def update_meter_task_from_server(meter_task_id, task_id, meter_id, meter_remark):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meter_task (id, meter_id, task_id, remark_meter)
        values
        ({meter_task_id}, '{meter_id}', {task_id},  '{meter_remark}')
        on conflict(id) do update set
            id = {meter_task_id},
            task_id = {task_id},
            meter_id = '{meter_id}', 
            remark_meter = '{meter_remark}' """
        cursor.execute(query)
        db.commit()


def update_meter_data_from_server(meter_number, instalation_day, meter_type, marka_id, marka, seal_number,
                                  date_next_verification, location, antimagnetic_protection,
                                  average_consumption):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meters (meter_number, instalation_date, type_service, marka_id, marka_name, seal_number, 
        date_of_death, location, antimagnetic_protection, average_consumption)
        values
        ('{meter_number}', '{instalation_day}', '{meter_type}', '{marka_id}', '{marka}', '{seal_number}', 
        '{date_next_verification}', '{location}', '{antimagnetic_protection}', {average_consumption})
        on conflict(meter_number) do update set
            instalation_date = '{instalation_day}', 
            type_service = '{meter_type}', 
            marka_name = '{marka}', 
            marka_id = '{marka_id}',
            seal_number = '{seal_number}', 
            date_of_death = '{date_next_verification}', 
            location = '{location}',
            antimagnetic_protection = '{antimagnetic_protection}', 
            average_consumption = {average_consumption} """
        cursor.execute(query)
        db.commit()


def update_meter_reading_data_from_server(id_meter_reading, meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meter_reading (id, meter_id, last_reading_date, last_reading_value)
        values
        ({id_meter_reading}, '{meter_id}', '{reading_date}', '{reading_values}')
        on conflict(id) do update set
            meter_id = '{meter_id}', 
            last_reading_date = '{reading_date}', 
            last_reading_value = '{reading_values}' """
        cursor.execute(query)
        db.commit()


def update_seal(seal_number, meter_id, task_id, remark, meter_reading, seal_type):  # seal_type задел на будующее
    with sl.connect('database_client.db') as db:
        today_seal = datetime.datetime.now().strftime("%Y-%m-%d")
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = db.cursor()
        query1 = f""" update meter_reading set  
                            new_reading_date = '{today_seal}',
                            new_reading_value = '{meter_reading}'
                            where meter_id = '{meter_id}' """
        cursor.execute(query1)
        db.commit()
        query2 = f""" update meters set  
                            status_filling = 'выполнен',
                            seal_number = '{seal_number}'
                            where meter_number = '{meter_id}' """
        cursor.execute(query2)
        db.commit()
        query = f""" update meter_task set  
                            remark_meter = '{remark}'
                            where meter_id = '{meter_id}' """
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
                           unloading_time = '{str(today)}',  
                           status = 'в исполнении',
                           unloaded = false
                           where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(task_id if isinstance(task_id, list) else [task_id])


def update_date(id_task, date):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
                           date = '{date}'  
                           where id = {id_task} """
        cursor.execute(query)
        db.commit()


def update_acts_insert_meters(id_task, string, meter):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query = f""" select reason from acts where task_id = {id_task} """
        result = cursor.execute(query).fetchone()
        if result:
            new_reason = result[0] + string
            if meter:
                query = f""" update acts set reason = '{new_reason}', 
                                not_working_meters = COALESCE(not_working_meters, '') || '{meter}'
                            where task_id = {id_task} """
            else:
                query = f""" update acts set reason = '{new_reason}' where task_id = {id_task}"""
        else:
            if meter:
                query = f""" INSERT INTO acts 
                                    (task_id, date, reason, not_working_meters) 
                                    VALUES ({id_task}, '{today}', '{string}', '{meter}')"""
            else:
                query = f""" INSERT INTO acts 
                                     (task_id, date, reason) 
                                     VALUES ({id_task}, '{today}', '{string}')"""
        cursor.execute(query)
        db.commit()
        query = f""" update tasks set status = 'в испольнении'
                    where id = {id_task} and status != 'выполнен' """
        cursor.execute(query)
        db.commit()
        if scr.func.check_internet():
            scr.BD.bd_users.bd_server_user.unload_task(id_task if isinstance(id_task, list) else [id_task])


def update_photo_meter(last_meter_id, new_meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update picture_temp 
                        set meter_id = '{new_meter_id}'
                        where meter_id = '{last_meter_id}' """
        cursor.execute(query)
        db.commit()


def update_status_task():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ update tasks set
                            status = 'просрочен' 
                            where date_end < Date('now') and status != 'выполнен' and status != 'в исполнении' """
        cursor.execute(query)
        db.commit()


def update_upload_status_false(id_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set
                            unloaded = false
                            where id = {id_task}"""
        cursor.execute(query)
        db.commit()


def update_server_id_photo(id_photo, server_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" UPDATE picture 
                SET server_id = {server_id} 
                WHERE id = {id_photo} """
        cursor.execute(query)
        db.commit()


def update_upload_status_true(id_task):
    id_task = [int(i) for i in id_task]
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set
                            unloaded = true
                            where id in ({','.join(['?'] * len(id_task))})"""
        cursor.execute(query, id_task)
        db.commit()


def update_made_act_status(act_id, status):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update acts set
                                    made = {status}
                                    where id = {act_id} """
        cursor.execute(query)
        db.commit()


def update_act_status_unload(act_id):
    id_act = [int(i) for i in act_id]
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update acts set
                                    unloaded = True
                                    where id in ({','.join(['?'] * len(id_act))}) """
        cursor.execute(query, id_act)
        db.commit()

