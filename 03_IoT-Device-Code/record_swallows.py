import sounddevice as sd
from scipy.io.wavfile import write
import os
from time import time

fs = 8000  # Sample rate
seconds = 10  # Duration of recording

# DEVICE SELECTION: run
# python3 -m sounddevice
sd.default.device = 0
sd.default.samplerate = fs

# Set the file directory
unchunked_audio_directory_relative_path = "../audio_files/unchunked_audio_files/"
dirname = os.path.dirname(__file__)
unchunked_audio_directory_path = os.path.join(
    dirname, unchunked_audio_directory_relative_path)


while True:

    # Record:
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    # Save as .wav
    file_name = unchunked_audio_directory_path + str(int(time())) + ".wav"
    write(file_name, fs, recording)  # Save as WAV file
