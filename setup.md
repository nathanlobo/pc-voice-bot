###### WINDOWS SETUP ######

# 1. Install necessary Python libraries
pip install vosk sounddevice

# 2. Download the Vosk small English model
Invoke-WebRequest -Uri "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip" -OutFile "model.zip"

# 3. Extract the zip file
Expand-Archive -Path .\model.zip -DestinationPath .

# 4. Rename the extracted folder to 'model' so the script can find it
Rename-Item -Path .\vosk-model-small-en-us-0.15 -NewName model

# 5. Clean up the zip file (optional)
Remove-Item .\model.zip

# 6. List audio devices to find your Microphone ID
# Look for the number next to your mic and put it in the DEVICE_ID variable in your script
python -c "import sounddevice as sd; print(sd.query_devices())"

# 7. Run your script
python voice-control.py




### LINUX SETUP ###

# 1. Update system and install dependencies
sudo apt update && sudo apt install -y python3-pip libportaudio2
pip3 install vosk sounddevice

# 2. Download and unzip the model
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip

# 3. Rename folder and cleanup
mv vosk-model-small-en-us-0.15 model
rm vosk-model-small-en-us-0.15.zip

# 4. Find Microphone ID on the Pi
python3 -c "import sounddevice as sd; print(sd.query_devices())"

# 5. Run your script
python3 voice-control.py