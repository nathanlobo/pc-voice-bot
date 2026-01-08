import speech_recognition as sr
import pyttsx3
import os
import sys
import json
import time
import webbrowser
import threading
import pygame

# --- CONFIGURATION ---
MUSIC_FOLDER = r"C:\Users\nathan\Music\_Vibe" # Ensure this path is correct
DEFAULT_BOT_NAME = "Jarvis"

# --- GLOBAL VARIABLES ---
engine = pyttsx3.init()
engine.setProperty('rate', 170) 
engine.setProperty('volume', 1.0)

# Music State
current_track_index = 0
music_files = []
paused = False
music_stopped = False
mixer_initialized = False

# --- SYSTEM FUNCTIONS ---

def speak(text):
    print(f"[BOT]: {text}")
    engine.say(text)
    engine.runAndWait()

def ensure_bot_data():
    if not os.path.exists("botData.json"):
        with open("botData.json", "w") as f:
            json.dump({"name": DEFAULT_BOT_NAME}, f)

def get_bot_name():
    ensure_bot_data()
    try:
        with open("botData.json", "r") as f:
            data = json.load(f)
            return data.get("name", DEFAULT_BOT_NAME)
    except:
        return DEFAULT_BOT_NAME

def listen_input(prompt=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if prompt: print(prompt)
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source)
        
        try:
            # Listening for command
            audio = r.listen(source, timeout=None, phrase_time_limit=6)
            query = r.recognize_google(audio, language="en-in")
            print(f"[USER]: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Connection error.")
            return None

# --- MUSIC FUNCTIONS ---

def init_music():
    global mixer_initialized, music_files
    if not mixer_initialized:
        try:
            pygame.mixer.init()
            mixer_initialized = True
        except Exception as e:
            print(f"Mixer Error: {e}")
            return False
            
    if not os.path.exists(MUSIC_FOLDER):
        speak("Music folder not found.")
        return False
        
    supported = ('.mp3', '.wav', '.ogg')
    music_files = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(supported)]
    
    if not music_files:
        speak("No music files found.")
        return False
    return True

def play_music_logic():
    global current_track_index, paused, music_stopped
    if not init_music(): return

    while not music_stopped:
        if not paused:
            if not pygame.mixer.music.get_busy():
                track_path = os.path.join(MUSIC_FOLDER, music_files[current_track_index])
                try:
                    pygame.mixer.music.load(track_path)
                    pygame.mixer.music.play()
                    print(f"Playing: {music_files[current_track_index]}")
                    
                    while pygame.mixer.music.get_busy() or paused:
                        if music_stopped: break
                        time.sleep(1)
                    
                    if not music_stopped:
                        current_track_index = (current_track_index + 1) % len(music_files)
                except Exception as e:
                    print(f"Playback error: {e}")
                    break
        else:
            time.sleep(1)

def start_music_thread():
    global music_stopped, paused
    music_stopped = False
    paused = False
    t = threading.Thread(target=play_music_logic)
    t.daemon = True
    t.start()

# --- COMMAND PROCESSING ---

def process_command(command):
    global paused, music_stopped, current_track_index
    
    sites = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "instagram": "https://instagram.com",
        "facebook": "https://facebook.com",
        "whatsapp": "https://web.whatsapp.com",
        "chatgpt": "https://chatgpt.com",
        "gmail": "https://mail.google.com",
        "gemini": "https://gemini.google.com",
        "google docs": "https://docs.google.com",
        "spreadsheet": "https://docs.google.com/spreadsheets",
        "google keep": "https://keep.google.com",
        "presentation": "https://docs.google.com/presentation"
    }

    if "play music" in command:
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            speak("Resuming music.")
        else:
            start_music_thread()
            speak("Playing music.")
        
    elif "pause music" in command:
        paused = True
        pygame.mixer.music.pause()
        speak("Music paused.")
        
    elif "resume music" in command:
        paused = False
        pygame.mixer.music.unpause()
        speak("Resuming music.")
        
    elif "next music" in command:
        pygame.mixer.music.stop()
        current_track_index = (current_track_index + 1) % len(music_files)
        # Thread loop handles restart
        
    elif "previous music" in command:
        pygame.mixer.music.stop()
        current_track_index = (current_track_index - 1) % len(music_files)

    elif "change bot name" in command:
        speak("What should I be called?")
        new_name = listen_input()
        if new_name:
            with open("botData.json", "w") as f:
                json.dump({"name": new_name}, f)
            speak(f"Name changed to {new_name}")

    elif "open" in command:
        for site_name, url in sites.items():
            if site_name in command:
                speak(f"Opening {site_name}")
                webbrowser.open(url)
                return

    elif "shutdown" in command or "go to sleep" in command:
        speak("Shutting down. Goodbye.")
        os._exit(0)

# --- MAIN LOOP ---

def main():
    bot_name = get_bot_name()
    speak(f"{bot_name} is online and listening.")
    
    while True:
        print(f"\n[{bot_name}]: Listening for command...")
        command = listen_input()
        
        if command:
            # If user calls the bot by name (e.g., "Jarvis, play music")
            if bot_name.lower() in command:
                # Optional: You can make it ask "Yes boss?" here, or just process the command directly.
                # Currently, it checks if there is a command included with the name.
                
                # If command is JUST the name (e.g. "Jarvis"), ask for input
                if command.strip() == bot_name.lower():
                    speak("Yes?")
                    specific_cmd = listen_input()
                    if specific_cmd:
                        process_command(specific_cmd)
                else:
                    # If command is "Jarvis open youtube", process it
                    process_command(command)
            else:
                # Also process direct commands without name (e.g. "Open Youtube")
                process_command(command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")