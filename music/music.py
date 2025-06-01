from pywhatkit import playonyt

def play_song(song_name):
    playonyt(song_name)

while True:
    x = input("Enter the song name: ")
    play_song(x)