from plyer import notification

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Karen",
        #app_icon="C:\Users\ABC\Downloads\karen.png",
        timeout=5
    )
