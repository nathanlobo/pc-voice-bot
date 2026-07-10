import os
import json
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# 1. Setup the Queue and Callback for audio data
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# 2. Configuration
MODEL_PATH = "model" # Path to the unzipped model folder
SAMPLE_RATE = 16000  # Standard for Vosk small models
DEVICE_ID = None     # Use None for default, or integer for specific USB mic

if not os.path.exists(MODEL_PATH):
    print(f"Please download the model from alphacephei.com/vosk/models and unpack as '{MODEL_PATH}'")
    sys.exit(1)

# 3. Initialize Model and Recognizer
# We pass a JSON list of strings to restrict the vocabulary (Grammar)
model = Model(MODEL_PATH)
commands = '["turn right", "turn left", "forward", "backward", "g turn", "[unk]"]'
rec = KaldiRecognizer(model, SAMPLE_RATE, commands)

print(f"\n--- System Ready ---")
print(f"Listening for: {commands}\n")

try:
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, device=DEVICE_ID, 
                           dtype='int16', channels=1, callback=callback):
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # result contains the full sentence
                result = json.loads(rec.Result())
                text = result.get("text", "")
                
                if text:
                    print(f"Detected: {text.upper()}")
            else:
                # PartialResult can be checked here if you want real-time feedback
                pass

except KeyboardInterrupt:
    print("\nStopping...")
except Exception as e:
    print(f"Error: {e}")