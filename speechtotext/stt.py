import speech_recognition as sr # type: ignore
import os
import threading

from colorama import Fore, Back, Style, init # type: ignore
init(autoreset=True)


def print_loop () :
    while True:
        print(Fore.GREEN + "Listening...", end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)

def listen():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 300
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    r.pause_threshold = 0.8
    r.operation_timeout = None

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("\r" + " " * 80, end="\r") #clear the line
            print(Fore.GREEN + "Listening...", end="", flush=True)
            try:
                audio = r.listen(source,timeout=None)
                print("\r" + Fore.LIGHTBLACK_EX + "recognizing...",end="",flush=True)
                query = r.recognize_google(audio).lower()
                if query :
                    print("\r" + Fore.BLUE + f"Sir : {query}", end="", flush=True)
                    return query
                else:
                    print("\r" + Fore.RED + "No speech detected", end="", flush=True)
                    return ""
            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("\r", end="", flush=True)

            os.system("cls" if os.name == "nt" else "clear")
        speechtotextth = threading.Thread(target=listen)
        print_thread = threading.Thread(target=print_loop)
        speechtotextth.start()
        print_thread.start()
        speechtotextth.join()
        print_thread.join()

        

