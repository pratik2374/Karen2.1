import psutil
import time
from notification import notify

def battery_status():
    battery = psutil.sensors_battery()
    time.sleep(10)
    if int(battery.percent) == 100:
        print("Battery is FULL")
        notify("Battery is FULL", "Please unplug the charger")



battery_status()
