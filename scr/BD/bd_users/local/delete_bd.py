import sqlite3 as sl


def delete_data_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        delete_user = """ Delete from user """
        delete_task = """ Delete from tasks """
        delete_address = """ Delete from address """
        delete_meters = """ Delete from meters """
        delete_meter_task = """ Delete from meter_task """
        delete_meter_reading = """ Delete from meter_reading """
        delete_photo = """ Delete from picture """
        cursor.execute(delete_user)
        cursor.execute(delete_meters)
        cursor.execute(delete_meter_task)
        cursor.execute(delete_meter_reading)
        cursor.execute(delete_task)
        cursor.execute(delete_address)
        cursor.execute(delete_photo)


def delete_photo_db(id_photo):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        delete_photo = f""" Delete from picture where id = {id_photo}"""
        cursor.execute(delete_photo)
