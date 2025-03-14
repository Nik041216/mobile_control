import os

import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.create_bd
import scr.BD.bd_users.local.update_bd
import scr.func
import scr.navigation_apps.navigations
import scr.BD.bd_users.api_user


async def check_user_credentials(login, password, page):
    employee = scr.BD.bd_users.api_user.check_user(login, password)
    if employee:
        await scr.BD.bd_users.api_user.start_websocket(login, password, employee['employee_id'])
        print(employee)
        scr.BD.bd_users.local.create_bd.local_user_db()
        scr.navigation_apps.navigations.create_route(page)
        if employee['privileges'] == 2:
            scr.BD.bd_users.local.insert_bd.insert_bd_user(
                employee['employee_id'], employee['login'], password,
                employee['privileges'], employee['first_name'], employee['last_name'], page
            )
    else:
        scr.func.show_snack_bar(page, "Нет пользователя в базе данных")  # Нормально написать
        pass
