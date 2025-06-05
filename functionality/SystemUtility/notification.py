from win10toast_click import ToastNotifier
import webbrowser

# def on_notification_click():
#     print("Notification clicked!")
#     # You can open a URL or run any function
#     webbrowser.open("https://google.com")
#     return 0

def notify(message):
    toaster = ToastNotifier()
    toaster.show_toast(
    title="karen",
    msg=message,
    icon_path="SystemUtility\\logo.ico",  # use a .ico file for best results
    duration=1,
    threaded=True,
    #callback_on_click=on_notification_click
)
