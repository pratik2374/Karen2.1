import win32com.client # type: ignore

speaker = win32com.client.Dispatch("SAPI.SpVoice")
voices = speaker.GetVoices()
speaker.Voice = voices[3]
#print all voices and select the suitable one
# for i, voice in enumerate(voices):
#     print(f"Voice {i}: {voice.GetDescription()}")

def speak(text):
    speaker.Speak(text)

def is_command_in_query(command, query):
    return command.lower() in query.lower()


#Current voice is Microsoft Catherine - English (Australia)
speak("You know we could Die anytime and there's some million possibilities, still....., Sir! I'm KAREN, always ready to assist to in Best way I can..")

    
