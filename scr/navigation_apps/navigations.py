import scr.navigation_apps.users.pages.main_users_screen
import scr.navigation_apps.users.pages.user_setting_screen
import scr.navigation_apps.users.pages.ratyng_user_screen
import scr.navigation_apps.users.pages.future_user_screen
import scr.func
import flet as ft


# тут программа смотрит какая роль у человека
def role_definition(privileges, page):
    if privileges == 1:
        scr.func.show_alert_yn(page, "Вы не можете сейчас воспользоваться этим функционалом")
    elif privileges == 2:
        page.go("/")
    else:
        debugging()


def debugging():
    print('Тут можно добавить инфу по приложению, может быть обратную связь')

