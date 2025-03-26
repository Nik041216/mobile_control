import sqlite3 as sl


def select_user_data():
    try:
        with sl.connect('database_client.db') as db:
            cursor = db.cursor()
            query = """ Select id, login, password, privileges, last_name, first_name from user """
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as ex:
        return False


def select_task_ids():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select id from tasks """
        cursor.execute(query)
        result = cursor.fetchall()
        task_ids = [item[0] for item in result]
        return task_ids


def select_meters_data_new(id_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select m.* from meters as m
          left join meter_task as mt on mt.meter_id = m.meter_number
          where mt.task_id ={id_task} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_meter_reading_new(meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select meter_id, last_reading_date, last_reading_value, 
            new_reading_date, new_reading_value from meter_reading 
          where meter_id = '{meter_id}' """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_tasks_data_new(sorting, search_value, date):
    search_value = search_value.lower()
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select t.id|| '', t.fio, a.district, a.hamlet, a.street, a.dom, a.apartment, t.phone_number, 
                    t.personal_account || '', t.date, t.date_end, t.remark_task, t.status, t.purpose, 
                    a.registered_residing '', a.standarts '', a.area|| '', t.saldo 
                    from tasks as t
                    join address as a on a.id = t.id_address """
        if date == "future":
            query += f""" where t.date > current_date"""
        else:
            query += f""" where t.date <= current_date and current_date <= t.date_end"""
        if sorting == "Адрес":
            query += f""" order by a.street, a.dom, a.apartment"""
        elif sorting == "Дата":
            query += f""" order by t.date """
        else:
            query += f""" order by t.status"""

        cursor.execute(query)
        result = cursor.fetchall()

        filtered_result = [
            row for row in result if
            search_value in row[2].lower() or  # a.district
            search_value in row[3].lower() or  # a.hamlet
            search_value in row[4].lower() or  # a.street
            search_value in row[5].lower()  # a.dom
        ]

        return filtered_result


def select_tasks_data_for_one(id_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select a.id, t.id|| '', t.fio, a.street, a.dom, a.apartment, t.phone_number, 
        t.personal_account || '', t.date, t.date_end, t.remark_task, t.status, t.purpose, a.registered_residing|| '', 
        a.standarts|| '', a.area|| '', t.saldo, a.type_address from tasks as t
            join address as a on a.id = t.id_address 
            where t.id = {id_task} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_meters_data_new_for_one(id_task, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select m.*, mt.remark_meter from meters as m
          left join meter_task as mt on mt.meter_id = m.meter_number
          where mt.task_id ={id_task} and mt.meter_id = '{meter_id}' """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_data_to_upload():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ 
        SELECT 
            t.id, t.unloading_time, mr.new_reading_value, mr.new_reading_date, t.remark_task, t.status, mt.meter_id, 
            mt.remark_meter, t.purpose, m.seal_number, m.marka_name, m.antimagnetic_protection,
            m.type_service, t.id_address
        FROM tasks AS t
        JOIN meter_task AS mt ON mt.task_id = t.id
        JOIN meters AS m ON mt.meter_id = m.meter_number
        left JOIN meter_reading AS mr ON mr.meter_id = mt.meter_id;"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_task_for_upload(id_task):
    id_task = [int(i) for i in id_task]
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        SELECT 
            t.id, t.unloading_time, mr.new_reading_value, mr.new_reading_date, t.remark_task, t.status, mt.meter_id, 
            mt.remark_meter, t.purpose, m.seal_number, m.marka_name, m.antimagnetic_protection,
            m.type_service, t.id_address
        FROM tasks AS t
        JOIN meter_task AS mt ON mt.task_id = t.id
        JOIN meters AS m ON mt.meter_id = m.meter_number
        left JOIN meter_reading AS mr ON mr.meter_id = mt.meter_id
        where t.id in ({','.join(['?'] * len(id_task))})"""
        cursor.execute(query, id_task)
        result = cursor.fetchall()
        return result


def select_photo_data(meter_id, task_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" select * from picture where meter_id = '{meter_id}' and task_id = {task_id} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_photo_data_temp(meter_id, task_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" select * from picture_temp where meter_id = '{meter_id}' and task_id = {task_id} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_dop_data_to_upload():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select a.id, a.registered_residing, a.standarts, a.area, t.remark_task,t.id from address as a
                    join tasks as t on t.id_address = a.id"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_task_id():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select id from tasks where unloaded = 0 """
        cursor.execute(query)
        result = cursor.fetchall()
        task_ids = [item[0] for item in result]
        return task_ids
