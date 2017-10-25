import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import csv
import sys

data = ""
with open("data\sonata-beethoven\short\short-ps01_01.csv") as f:
    print("Reading from", f.name)
    r = csv.reader(f)
    for row in r:
        for item in row:
            for note in item:
                data = data + item
            data = data + chr(4000) # to differentiate timesteps

chars = sorted(list(set(data)))
VOCAB_SIZE = len(chars)

char_to_int = dict((c, i) for i, c in enumerate(chars)) # map each chr to int accessible by char
int_to_char = dict((i, c) for i, c in enumerate(chars)) # accessible by int

n_chars = len(data)
n_vocab = len(chars)

print("\nTotal Characters:", n_chars)
print("Total Vocab:", n_vocab)

seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
    seq_in = data[i:i + seq_length]
    seq_out = data[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns:", n_patterns)

X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
X = X / float(n_vocab)
y = np_utils.to_categorical(dataY)

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))  # Randomly deactivates certain neurons to prevent over fitting
model.add(Dense(y.shape[1], activation='softmax'))


def learn():
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    file_path ="weights/weights--{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(file_path, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    model.fit(X, y, epochs=5, batch_size=128, callbacks=callbacks_list) # Fit network to data


def create():
    filename = "weights/weights--04-3.3226.hdf5"
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')

    start = numpy.random.randint(0, len(dataX) - 1)
    pattern = dataX[start]
    print("Seed:")
    print(''.join([int_to_char[value] for value in pattern]))

    final = []
    for i in range(10000):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        pattern.append(index)
        pattern = pattern[1:len(pattern)]

        final.append(result)

    to_csv(final)


def to_csv(a):
    a_str = "".join(a)
    data = a_str.split(chr(4000))
    with open("output.csv", "w") as f:
        w = csv.writer(f)
        w.writerow(data)

if __name__ == "__main__":
    error = "\nUsage: lstm.py [action] \nlearn/ create"
    if sys.argv[1] == "learn":
        learn()
    elif sys.argv[1] == "create":
        create()