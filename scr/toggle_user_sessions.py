import os

import scr.BD.bd_users.bd_server_user
import scr.BD.bd_users.local.select_bd
import scr.func
import scr.navigation_apps.navigations
import scr.verifications


def handle_user_sessions(page):
    if os.path.exists("database_client.db"):
        if scr.BD.bd_users.local.select_bd.select_user_data():
            result = scr.BD.bd_users.local.select_bd.select_user_data()
        if result:  # Проверяем, что содержимое не пустое
            for record in result:
                login = record[1]
                password = record[2]
                privileges = record[3]
                if login != "" and password != "":
                    scr.navigation_apps.navigations.role_definition(privileges, page)
                    scr.func.show_snack_bar(page, "Успешний вход в систему.")
                else:
                    scr.verifications.authentication(page)
        else:
            scr.verifications.authentication(page)
    else:
        scr.verifications.authentication(page)
