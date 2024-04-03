# for the ML
from pydub import AudioSegment
from joblib import load
import librosa  # to extract speech features
from numpy import mean, asarray
import os
import csv
dirname = os.path.dirname(__file__)

# The relative paths
unchunked_audio_directory_relative_path = "../audio_files/unchunked_audio_files/"
chunked_audio_directory_relative_path = "../audio_files/chunked_audio_files/"
audio_chunks_directory_relative_path = "../audio_files/audio_chunks/"
ML_temp_directory_relative_path = "../audio_files/ML_temp_audio/"
unuploaded_database_relative_path = "../database/unuploaded_database.csv"

unchunked_audio_directory_path = os.path.join(
    dirname, unchunked_audio_directory_relative_path)
chunked_audio_directory_path = os.path.join(
    dirname, chunked_audio_directory_relative_path)
audio_chunks_directory_path = os.path.join(
    dirname, audio_chunks_directory_relative_path)
ML_temp_directory_path = os.path.join(
    dirname, ML_temp_directory_relative_path)
unuploaded_database_path = os.path.join(
    dirname, unuploaded_database_relative_path)
model_path = os.path.join(
    dirname, "ML_swallow_classifier_model.joblib")


# Load the previously trained model
model = load(model_path)

# Set the duration of the audio files
raw_audio_duration = 5000
audio_chunk_duration = 200
ML_input_audio_duration = 3000


def classify_swallow(file_path):
    swallow_audio_mfcc_data = (extract_mfcc(file_path))
    swallow_audio_mfcc_data_array = asarray(
        swallow_audio_mfcc_data)  # convert the input to an array

    # Convert the data in the form X = [n_samples, n_features (in this case, 40)]
    swallow_audio_mfcc_data_array = swallow_audio_mfcc_data_array.reshape(
        1, -1)

    # Predicts which of the classes (in this case 2) the sample belongs to
    return model.predict(swallow_audio_mfcc_data_array)[0]


def extract_mfcc(wav_file_name):
    # This function extracts mfcc features and obtain the mean of each dimension
    y, sr = librosa.load(wav_file_name)
    mfccs = mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)

    return mfccs


def update_database(chunk_ID):
    # Find the time and date of the swallow from the file name
    UNIX_Time = int(chunk_ID.rpartition(
        '_')[0]) + int(int(chunk_ID.rpartition('_')[2].rpartition('.')[0]) * audio_chunk_duration/1000)
    with open(unuploaded_database_path, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = csv.writer(write_obj)
        # Add date and time of swallow
        csv_writer.writerow([UNIX_Time])


# Split the raw audio rercordings in 200ms intervals. This is because that's faster than a swallow
unchunked_files_list = os.listdir(unchunked_audio_directory_path)

for unchunked_file in unchunked_files_list:

    unchunked_file_no_extension = unchunked_file.rpartition('.')[0]

    # Create an AudioSegment object
    unchunked_audio = AudioSegment.from_wav(
        unchunked_audio_directory_path + unchunked_file)

    # Slice into segments
    for chunk_counter in range(int(raw_audio_duration / audio_chunk_duration)):
        chunk = unchunked_audio[chunk_counter *
                                audio_chunk_duration: (chunk_counter+1)*audio_chunk_duration]

        # Export to a wav file
        chunk.export(audio_chunks_directory_path + unchunked_file_no_extension + "_" +
                     str(chunk_counter).zfill(4) + ".wav", format="wav")

    # Move the file to the folder of the already chunked files
    os.rename(unchunked_audio_directory_path + unchunked_file,
              chunked_audio_directory_path + unchunked_file)

print("files chunked")
# Create a queue that has the length required by the ML algorithm
chunks_list_length = int(ML_input_audio_duration / audio_chunk_duration)
# chunks_queue = queue.Queue(queue_length)
chunks_list = []


# Create a list of chunks

chunks_directory_names_list = sorted(filter(lambda x: os.path.isfile(os.path.join(
    audio_chunks_directory_path, x)), os.listdir(audio_chunks_directory_path)))

# chunks_directory_names_list = chunks_directory_names_list.sort()
# Fill the queue with chunks
for i in range(chunks_list_length):
    chunks_list.append(chunks_directory_names_list[i])
print("queue filled")

while len(chunks_directory_names_list) > chunks_list_length:

    ML_chunk = AudioSegment.empty()
    for listElement in chunks_list:
        # Construct the audio chunk that will be fed into the ML model
        ML_chunk += AudioSegment.from_wav(audio_chunks_directory_path +
                                          listElement)

    chunk_id = chunks_list[0]

    ML_file_handle = ML_chunk.export(
        ML_temp_directory_path + chunk_id, format="wav")
    print("classifying")
    classification = classify_swallow(ML_file_handle)

    print("result" + str(classification))
    classification = classification[0]
    if classification:
        update_database(chunk_id)

    item = chunks_directory_names_list.pop(0)
    del chunks_list[0]
    # Update queue with next 200ms segment
    chunks_list.append(chunks_directory_names_list[len(chunks_list)])

    # delete the 200 ms chunk from the folder
    print("deleting" + item)
    os.remove(ML_temp_directory_path + item)
    os.remove(audio_chunks_directory_path + item)

for j in range(chunks_list_length):
    os.remove(audio_chunks_directory_path + chunks_directory_names_list.pop())
