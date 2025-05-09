import speech_recognition as sr
import os, sys, subprocess, json
import time
import webbrowser
import threading
import pygame, pyaudio

# Global variables to manage music playback
current_track_index = 0
music_files = []
paused = False
music_stopped = False

# Defining folder & file paths here
music_folder = r'C:\Users\nathan\Music\Fav'

def restartProgram():
    try:
        python = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Script not found at {script_path}")
        subprocess.call([python, script_path] + sys.argv[1:])
        sys.exit()  # Exit the current script after restart
    except Exception as e:
        print(f"Error restarting the program: {e}")
def say(text):
    os.system(f'powershell -Command "Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"')
    # os.system(f'say "{text}"')
def takeCommand():
    try:
        r = sr.Recognizer()
        # command = input("Enter command: ")
        with sr.Microphone() as source:
            r.pause_threshold =  0.6
            audio = r.listen(source,timeout=5)
        print("Recognizing...")
        heardText = "Initial Text"
        heardText = r.recognize_google(audio, language="en-in")
        if heardText == "" or heardText == None or heardText == " ":
            takeCommand()
            print("retaking command")
        else:
            command = heardText.lower()
            print(f"User said: {heardText}")
            print(f"User said: {command}")
            return command
    except sr.WaitTimeoutError:
        takeCommand()
    except sr.UnknownValueError:
        print("Could not understand audio")
        takeCommand()
    except sr.RequestError as e:
        print(f"Error:{e}")

def wait_for_call():
    print("Wait call func started")
    command = takeCommand()
    print(command)
    if command == get_bot_data("name").lower():
        say(f"Yes Boss?")
        return True


def initialize_mixer():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print(f"Error initializing mixer: {e}")
        return False
    return True

def load_music_files():
    global music_files
    supported_formats = ('.mp3', '.wav', '.ogg')
    
    music_files = [f for f in os.listdir(music_folder) if f.endswith(supported_formats)]

    if not music_files:
        print("No music files found in the specified folder.")
        return False

    # random.shuffle(music_files)
    return True

def play_music():
    global current_track_index, paused, music_stopped

    if not initialize_mixer():
        return
    if not load_music_files():
        return

    while True:
        if not paused and not music_stopped:
            file_path = os.path.join(music_folder, music_files[current_track_index])
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except pygame.error as e:
                print(f"Error loading or playing the file: {e}")
                return

            while pygame.mixer.music.get_busy() or paused:
                if music_stopped:
                    return
                time.sleep(1)

            if not paused and not music_stopped:
                current_track_index = (current_track_index + 1) % len(music_files)

def play_music_thread():
    global music_stopped
    music_stopped = False
    music_thread = threading.Thread(target=play_music)
    music_thread.start()

def pause_music():
    global paused
    if not paused:
        pygame.mixer.music.pause()
        paused = True
    else:
        print("Music is already paused.")

def resume_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()  # This resumes the song from where it was paused
        paused = False
    else:
        print("Music is already playing.")

def next_music():
    global current_track_index, paused, music_stopped
    if len(music_files) > 1:
        pygame.mixer.music.stop()  # Stop current song
        current_track_index = (current_track_index + 1) % len(music_files)  # Move to next song
        paused = False
        music_stopped = False
        play_music_thread()  # Play the next song
    else:
        print("No more tracks in the playlist.")

def previous_music():
    global current_track_index, paused, music_stopped
    if len(music_files) > 1:
        pygame.mixer.music.stop()  # Stop current song
        # Move to the previous track, but make sure it's in range
        current_track_index = (current_track_index - 1) % len(music_files)
        paused = False
        music_stopped = False
        play_music_thread()  # Play the previous song
    else:
        print("No previous tracks in the playlist.")

def change_bot_name():
    global botName
    say("What should I name the bot?")
    command = takeCommand()
    botName["name"] = command
    with open("botData.json", "w") as f:
        json.dump(botName, f, indent=4)
    with open("botData.json", "r") as f:
        botName = json.load(f)
    say(f"Your bot is named {botName}")
    print(f"Your bot is named {botName}")

def get_bot_data(valName):
    with open("botData.json", "r") as f:
        botData = json.load(f)
    return botData[valName]

def processTask(command):
    print("Processing command")
    try:
        sites = [
                ["youtube", "https://youtube.com"],
                ["google", "https://google.com"],
                ["instagram", "https://instagram.com"],
                ["facebook", "https://facebook.com"],
                ["whatsapp", "https://web.whatsapp.com"],
                ["wikipedia", "https://wikipedia.org"],
                ["drive", "https://drive.google.com"],
                ["gmail", "https://mail.google.com"],
                ["chatgpt", "https://chatgpt.com"],
                ["spotify", "https://open.spotify.com"],
                ["gemini", "https://gemini.google.com"],
                ["google docs", "https://docs.google.com"],
                ["spreadsheet", "https://docs.google.com/spreadsheets"],
                ["google keep", "https://keep.google.com"],
                ["presentation", "https://docs.google.com/presentation"]
                ]
        if get_bot_data("name") in command:
            say("Yes Boss, Im listening.")
            processTask(takeCommand())
        elif "play music" in command:
            play_music_thread()
            print("Playing music")
        elif "pause music" in command:
            pause_music()
            print("Pausing Music")
        elif "resume music" in command:
            resume_music()
            print("Resuming music")
        elif "next music" in command:
            next_music()
            print("Playing next music")
        elif "previous music" in command:
            previous_music()
            print("Playing previous music")
        elif "change bot name" in command:
            change_bot_name()
        elif "open" in command:
            for site in sites:
                if f"open {site[0]}".lower() in command:
                    say(f"Opening {site[0]}")
                    webbrowser.open(site[1])
        else:
            print("Didn't do any task") 
    except sr.UnknownValueError:
        say("Could not understand audio, Repeat again")

def main():
    try:
        botName = get_bot_data("name")
        say(f"Intializing {botName}")
        while True:
            print("Waiting for call...")
            if wait_for_call():
                print(f"{botName} is called")
                command = takeCommand()
                processTask(command)
                print("Processed task")
    except KeyboardInterrupt:
        restartProgram()

if __name__ == "__main__":
    main()