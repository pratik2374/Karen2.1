import os
import subprocess
import tempfile
from playsound import playsound # pip install playsound==1.2.2
import threading

current_voice = 'en-US-JennyNeural'

def speak(text: str)->None:
    voice = current_voice
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            output_file = tmpfile.name

        command = f'edge-tts --voice {voice} --text "{text}" --write-media {output_file}'

        subprocess.run(command, shell=True, check=True)

        threading.Thread(target=playsound, args=(output_file,)).start()

    except Exception as e:
        print(e)

def speak2(text: str, current_voice)->None:
    voice = current_voice
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
            output_file = tmpfile.name

        command = f'edge-tts --voice {voice} --text "{text}" --write-media {output_file}'

        subprocess.run(command, shell=True, check=True)

        threading.Thread(target=playsound, args=(output_file,)).start()

    except Exception as e:
        print(e)

# voice = 0
# print(voice)


# # we can choose the voice from the list of voices from here : https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462
# query = input("Enter a text to speak: ")
# while True:
#     print(current_voice + " " + str(voice))
#     speak(query, current_voice)
#     current_voice = input("Enter a voice: ")
#     voice += 1

