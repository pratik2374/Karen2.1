import psutil
import time
from notification import notify

def battery_status(alert: bool = True, current: bool = True) -> None:
    battery = psutil.sensors_battery()
    if alert == True:
        if int(battery.percent) == 100:
            print("Battery is FULL")
            notify("Battery is FULL", "Please unplug the charger")
        else:
            if current == True:
                print("Battery is not full")
                notify(f"Battery is {battery.percent}% charged")
                
    time.sleep(10)
        



battery_status()
