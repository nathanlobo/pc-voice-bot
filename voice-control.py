import speech_recognition as sr

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 4000  # Lower sensitivity for clearer detection
recognizer.pause_threshold = 0.8    # Slightly longer pause to confirm speech end
recognizer.phrase_threshold = 0.3   # Require more audio to start recognizing
recognizer.non_speaking_duration = 0.5  # Wait longer for trailing silence

COMMAND_RESPONSES = {
    "turn right": "turning right",
    "turn left": "turning left",
    "forward": "moving forward",
    "backward": "moving backward",
    "g turn": "doing a g turn",
}

def listen_input(prompt=None):
    with sr.Microphone() as source:
        if prompt:
            print(prompt)
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Better calibration
        except Exception:
            pass
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            try:
                query = recognizer.recognize_google(audio, language="en-in")
            except sr.UnknownValueError:
                query = recognizer.recognize_google(audio, language="en-US")
            query = query.strip()
            if query:
                print("[STATUS]: Speech detected. Processing...")
                return query.lower()
            return None
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Connection error.")
            return None

def process_command(command):
    command = " ".join(command.split())
    print(f"[DETECTED]: {command}")
    response = COMMAND_RESPONSES.get(command)
    if response:
        print(f"[BOT]: {response}")
    else:
        print("[BOT]: Command not recognized.")

def main():
    print("[BOT]: Listening for movement commands.")
    
    while True:
        command = listen_input()
        if command:
            process_command(command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")