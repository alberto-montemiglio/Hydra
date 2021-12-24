import numpy as np  # linear algebra
import librosa  # to extract speech features

# MLP Classifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

from joblib import dump
from tensorflow.keras.utils import to_categorical


recordings_path = os.path.dirname(__file__)


def extract_mfcc(wav_file_name):
 
    # This function extracts mfcc features and obtain the mean of each dimension

    y, sr = librosa.load(wav_file_name)
    mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)

    return mfccs


# Declare types of swallow:

swallow_types = ["Water", "Empty", "Food", "Other"]
swallow_types_labels = range(len(swallow_types))

swallow_labels = []
swallow_audio_mfcc_data = []


# Load the database and extracf mfcc features:

for label in swallow_types_labels:
    swallow_type = swallow_types[label]
    counterFileString = recordings_path + "/Recordings_" + swallow_type + \
        "/counterfile_" + swallow_type + ".txt"
    with open(counterFileString, "r") as counterFile:

        for line in counterFile:
            counter = int(line)

    for i in range(0, counter):
        wav_file_name = recordings_path + "/Recordings_" + swallow_type + "/wav_" + swallow_type + \
            "/output_sounddevice_wav_" + swallow_type + "_" + str(i) + ".wav"

        swallow_labels.append(label)
        swallow_audio_mfcc_data.append(extract_mfcc(wav_file_name))


# convert data and label to array

swallow_audio_mfcc_data_array = np.asarray(swallow_audio_mfcc_data)  # convert the input to an array
swallow_labels_array = np.array(swallow_labels)

swallow_labels_array[swallow_labels_array > 0] = 1



# get tuple of array dimensions

swallow_labels_array.shape  


# make categorical labels

labels_categorical = to_categorical(swallow_labels_array)

swallow_audio_mfcc_data_array.shape
labels_categorical.shape


x_train, x_test, y_train, y_test = train_test_split(np.array(
    swallow_audio_mfcc_data_array), labels_categorical, test_size=0.20)


model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-06,

                      hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)


# Train the model

model.fit(x_train, y_train)


# Predict for the test set

y_pred = model.predict(x_test)


# Calculate the accuracy of our model

accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)


# Print the accuracy

print("Accuracy: {:.2f}%".format(accuracy*100))


# Save model to file
dump(model, 'ml_model_train.joblib')
