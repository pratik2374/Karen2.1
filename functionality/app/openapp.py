import pyautogui as gui
import time

def openapp(appname):
    gui.press('win')
    time.sleep(0.5)
    gui.write(appname)
    time.sleep(0.5)
    gui.press('enter')

while True:
    x = input("Enter the app name: ")
    openapp(x)