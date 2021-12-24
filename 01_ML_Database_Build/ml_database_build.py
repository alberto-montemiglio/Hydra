# Save Audio files to make a database

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write


fs = 8000  # Sample rate
seconds = 3  # Duration of recording

# DEVICE SELECTION: run
# python3 -m sounddevice
sd.default.device = 0
sd.default.samplerate = fs

recordingTypeNumber = input(
    "0: Empty Swallow | 1: Food | 2: Water | 3: Noise | 4: Dump")
recordingTypes = ["Empty", "Food", "Water", "Other", "Dump"]
recordingType = recordingTypes[int(recordingTypeNumber)]

print("This will be a " + recordingType + "swallow")

# Get last counter for file naming
counterFileString = "./Recordings_" + recordingType + \
    "/counterfile_" + recordingType + ".txt"
with open(counterFileString, "r") as counterFile:
    for line in counterFile:
        counter = int(line)


# Record:
print("Start Recording file: " + str(counter))
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
print("Finished Recording")

# Save as .wav
wavString = "./Recordings_" + recordingType + "/wav_" + recordingType + \
    "/output_sounddevice_wav_" + recordingType + "_" + str(counter) + ".wav"
write(wavString, fs, recording)  # Save as WAV file

# Save as array into csv file
listString = "./Recordings_" + recordingType + "/list_" + recordingType + \
    "/output_sounddevice_list_" + recordingType + "_" + str(counter) + ".csv"
recording = np.asarray(recording)
np.savetxt(listString, recording, delimiter=",")


# Overwrite the Counter file
counterFile = open(counterFileString, "w")
newCounter = int(counter) + 1
counterFile.write(str(newCounter))
counterFile.close()
