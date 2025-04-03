import flet_onesignal as fos

ONESIGNAL_APP_ID = "cafa7a48-16ed-40fe-8f41-5dad633db2bb"

onesignal = fos.OneSignal(
    settings=fos.OneSignalSettings(app_id=ONESIGNAL_APP_ID),
)
