import sqlite3 as sl
import datetime


def update_local_tasks(unloading_time, task_id, reading_value, remark, meter_id):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query1 = f""" update meter_reading set  
                    new_reading_date = '{today}',
                    new_reading_value = '{reading_value}'
                    where meter_id = {meter_id} """
        query2 = f""" update meters set  
                    status_filling = 'выполнен',
                    meter_remark = '{remark}'
                    where id = {meter_id} """
        cursor.execute(query1)
        cursor.execute(query2)
        db.commit()

        query = f""" update tasks set 
                   unloading_time = '{unloading_time}',  
                   status = 'в_исполнении'
                   where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
            unloading_time = '{unloading_time}',  
            status = 'выполнен'
            where id = {task_id} and id IN (
              SELECT DISTINCT t.id
              FROM tasks t
              JOIN address a ON t.id_address = a.id
              JOIN meters m ON a.id = m.id_address
              WHERE NOT EXISTS (
                SELECT 1
                FROM meters m2
                WHERE m2.id_address = a.id
                AND NOT EXISTS (
                  SELECT 1
                  FROM meter_reading mr
                  WHERE mr.meter_id = m2.id
                  AND mr.new_reading_value IS NOT NULL
                )
              )
            );"""
        cursor.execute(query)
        db.commit()


def update_local_tasks_v2(unloading_time, task_id, reading_value, remark, meter_id):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query1 = f""" update meter_reading set  
                    new_reading_date = '{today}',
                    new_reading_value = '{reading_value}'
                    where meter_id = {meter_id} """
        query2 = f""" update meters set  
                    status_filling = 'выполнен'
                    where meter_number = {meter_id} """
        query3 = f""" update meter_task set  
                    remark_meter = '{remark}'
                    where meter_id = {meter_id} """
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        db.commit()

        query = f""" update tasks set 
                   unloading_time = '{unloading_time}',  
                   status = 'в_исполнении'
                   where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        query = f""" UPDATE tasks SET 
                    unloading_time = '{unloading_time}',  
                    status = 'выполнен'
                    WHERE id = {task_id} AND id IN (
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
                    ); """
        cursor.execute(query)
        db.commit()


def update_dop_data_address(remark, registered_residing, standarts, area, address_id, task_id, ):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
            remark = '{remark}'  
            where id = {task_id}"""
        cursor.execute(query)
        query1 = f""" update address set  
            registered_residing = '{int(registered_residing)}',
            standarts = '{standarts}',
            area = '{area}'
            where id = {address_id} """
        cursor.execute(query1)
        db.commit()


def update_dop_data_address_v2(remark, registered_residing, standarts, area, address_id, task_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
            remark_task = '{remark}'
            where id = {task_id} """
        cursor.execute(query)
        query1 = f""" update address set  
            registered_residing = {int(registered_residing)},
            standarts = {standarts},
            area = {area}
            where id = {address_id} """
        cursor.execute(query1)
        db.commit()


def update_tasks_data_from_server(task_id, name, address_id, city, district, street, dom, apartment, entrance,
                                  registered_residing, address_status, standarts, area, phone_number,
                                  personal_account, date_task, remark, status_task, purpose, saldo):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into tasks (id, name,id_address, phone_number,
                            personal_account, date, remark, status, purpose, saldo)
        values
        ({task_id}, '{name}', {address_id}, '{phone_number}','{personal_account}', '{date_task}', '{remark}', 
        '{status_task}', '{purpose}', '{saldo}')
        on conflict(id) do update set
            name = '{name}',
            id_address = {address_id}, 
            phone_number = '{phone_number}',
            personal_account = '{personal_account}',
            date = '{date_task}',
            remark =' {remark}',
            status = '{status_task}',
            purpose = '{purpose}',
            saldo = '{saldo}'"""
        cursor.execute(query)
        db.commit()
        query = f""" 
                insert into address (id, city, district, street, dom, apartment, entrance, registered_residing, status, 
                                    standarts, area)
                values
                ('{address_id}', '{city}', '{district}', '{street}', '{dom}', '{apartment}', '{entrance}', 
                {registered_residing}, '{address_status}', {standarts}, {area})
                on conflict(id) do update set
                    city = '{city}', 
                    district = '{district}', 
                    street = '{street}', 
                    dom = '{dom}', 
                    apartment = '{apartment}', 
                    entrance = '{entrance}', 
                    registered_residing = {registered_residing}, 
                    status = '{address_status}', 
                    standarts = {standarts}, 
                    area = {area}"""
        cursor.execute(query)


def update_tasks_data_from_server_v2(task_id, name, address_id, city, district, hamlet, street, dom, apartment,
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
            status = excluded.status,
            purpose = excluded.purpose,
            saldo = excluded.saldo
        """
        cursor.execute(query_tasks, (
            task_id, name, address_id, phone_number, personal_account,
            date_task, date_end, task_remark, status_task, purpose, saldo
        ))

        # Запрос для таблицы address
        query_address = """
        INSERT INTO address (id, city, district, hamlet, street, dom, apartment, entrance, registered_residing, standarts, area, type_address)
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


def update_meter_data_from_server(id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark,
                                  marka, seal_number, date_next_verification, location):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meters (id, meter_number, instalation_date, meter_type, id_address,
        marka, seal_number, date_next_verification, location,
        meter_remark)
        values
        ({id_meter}, '{meter_number}', '{instalation_day}', '{meter_type}', {id_address}, '{marka}', '{seal_number}', 
        '{date_next_verification}', '{location}', '{meter_remark}')
        on conflict(id) do update set
            meter_number = '{meter_number}', 
            instalation_date = '{instalation_day}', 
            meter_type = '{meter_type}', 
            id_address = {id_address},
            marka = '{marka}', 
            seal_number = '{seal_number}', 
            date_next_verification = '{date_next_verification}', 
            location = '{location}',
            meter_remark = '{meter_remark}'"""
        cursor.execute(query)
        db.commit()


def update_meter_task_from_server_v2(meter_task_id, task_id, meter_id, meter_remark):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meter_task (id, meter_id, task_id, remark_meter)
        values
        ({meter_task_id}, {task_id}, '{meter_id}', '{meter_remark}')
        on conflict(id) do update set
            id = {meter_task_id},
            task_id = {task_id},
            meter_id = {meter_id}, 
            remark_meter = '{meter_remark}' """
        cursor.execute(query)
        db.commit()


def update_meter_data_from_server_v2(meter_number, instalation_day, meter_type, marka_id, marka, seal_number,
                                     seal_date_instalation, date_next_verification, location, antimagnetic_protection,
                                     average_consumption):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meters (meter_number, instalation_date, type_service, marka_id, marka_name, seal_id, 
        seal_date_instalation, date_next_verification, location, antimagnetic_protection, average_consumption)
        values
        ('{meter_number}', '{instalation_day}', '{meter_type}', '{marka_id}', '{marka}', '{seal_number}', 
        '{seal_date_instalation}', '{date_next_verification}', '{location}', '{antimagnetic_protection}', 
        {average_consumption})
        on conflict(meter_number) do update set
            instalation_date = '{instalation_day}', 
            type_service = '{meter_type}', 
            marka_name = '{marka}', 
            marka_id = '{marka_id}',
            seal_id = '{seal_number}', 
            seal_date_instalation = '{seal_date_instalation}',
            date_next_verification = '{date_next_verification}', 
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
        ({id_meter_reading}, {meter_id}, '{reading_date}', '{reading_values}')
        on conflict(id) do update set
            meter_id = {meter_id}, 
            last_reading_date = '{reading_date}', 
            last_reading_value = '{reading_values}' """
        cursor.execute(query)
        db.commit()


def update_meter_reading_data_from_server_v2(id_meter_reading, meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meter_reading (id, meter_id, last_reading_date, last_reading_value)
        values
        ({id_meter_reading}, {meter_id}, '{reading_date}', '{reading_values}')
        on conflict(id) do update set
            meter_id = {meter_id}, 
            last_reading_date = '{reading_date}', 
            last_reading_value = '{reading_values}' """
        cursor.execute(query)
        db.commit()


def update_seal(seal_number, meter_id, task_id, remark):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query2 = f""" update meters set  
                            status_filling = 'выполнен',
                            seal_number = '{seal_number}'
                            meter_remark = '{remark}'
                            where id = {meter_id} """
        cursor.execute(query2)
        db.commit()

        query = f""" update tasks set 
                           unloading_time = '{str(today)}',  
                           status = 'в_исполнении'
                           where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
                            unloading_time = '{str(today)}',  
                            status = 'выполнен'
                            where id = {task_id} and id IN (
                              SELECT DISTINCT t.id
                              FROM tasks t
                              JOIN address a ON t.id_address = a.id
                              JOIN meters m ON a.id = m.id_address
                              WHERE m.status_filling = 'выполнен'
                            );
                  """
        cursor.execute(query)
        db.commit()


def update_seal_v2(seal_number, meter_id, task_id, remark):
    with sl.connect('database_client.db') as db:
        today_seal = datetime.datetime.now().strftime("%Y-%m-%d")
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = db.cursor()
        query2 = f""" update meters set  
                            status_filling = 'выполнен',
                            seal_id = '{seal_number}',
                            seal_date_instalation = '{str(today_seal)}'
                            where meter_number = {meter_id} """
        cursor.execute(query2)
        db.commit()
        query = f""" update meter_task set  
                            remark_meter = '{remark}'
                            where meter_id = {meter_id} """
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
                           unloading_time = '{str(today)}',  
                           status = 'в_исполнении'
                           where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
                            unloading_time = '{str(today)}',  
                            status = 'выполнен'
                            where id = {task_id} and id IN (
                              SELECT DISTINCT t.id
                              FROM tasks t
                              JOIN meter_task mt ON t.id = mt.task_id
                              JOIN meters m ON mt.meter_id = m.meter_number
                              WHERE m.status_filling = 'выполнен'
                            );
                  """
        cursor.execute(query)
        db.commit()


def update_date(id_task, date):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
                           date = '{date}'  
                           where id = {id_task} """
        cursor.execute(query)
        db.commit()
