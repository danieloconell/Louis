import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import csv
import convert_long
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("Action", help="Action to perform, learn or create")
parser.add_argument('--epochs', '-e', type=int, help="Number of epochs to be run", default=5)
parser.add_argument('--file', '-f', type=str, help="Weights for neural network")
parser.add_argument('--num', '-n', type=int, help="Number of songs to be made", default=1)
parser.add_argument('--length', '-l', type=int, help="Length per song", default=1000)

args = parser.parse_args()

if args.Action.lower() != "create" and args.Action.lower() != "learn":
    print("\nWrong Action Argument")
    quit()

data = ""
with open("data.csv") as f:
    print("Reading from", f.name)
    r = csv.reader(f)
    for row in r:
        for timestep in tqdm(row):
            data = data + timestep + chr(4000)  # to differentiate timesteps

chars = sorted(list(set(data)))
VOCAB_SIZE = len(chars)

char_to_int = dict((c, i) for i, c in enumerate(chars))  # map each chr to int accessible by char
int_to_char = dict((i, c) for i, c in enumerate(chars))  # accessible by int

n_chars = len(data)
n_vocab = len(chars)

print("\nTotal Characters:", n_chars)
print("Total Vocab:", n_vocab)

seq_length = 100
dataX = []
dataY = []

print("\nConverting Data")
for i in tqdm(range(0, n_chars - seq_length, 1)):
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
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
if args.file:
    model.load_weights(args.file)

model.compile(loss='categorical_crossentropy', optimizer='adam')


def learn():
    print("\n")
    file_path ="weights/weights--{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(file_path, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    model.fit(X, y, epochs=args.epochs, batch_size=128, callbacks=callbacks_list) # Fit network to data


def create(outputfile):
    start = numpy.random.randint(0, len(dataX) - 1)
    pattern = dataX[start]
    print("Seed:")
    print(''.join([int_to_char[value] for value in pattern]))

    final = []
    print("\nCreating Music")
    for i in tqdm(range(args.length)):
        x = numpy.reshape(pattern, (1, len(pattern), 1))
        x = x / float(n_vocab)
        prediction = model.predict(x, verbose=0)
        index = numpy.argmax(prediction)
        result = int_to_char[index]
        seq_in = [int_to_char[value] for value in pattern]
        pattern.append(index)
        pattern = pattern[1:len(pattern)]

        final.append(result)

    to_midi(final, outputfile)


def to_midi(a, name):
    a_str = "".join(a)
    data = a_str.split(chr(4000))
    with open(str(name)+".csv", "w") as f:
        w = csv.writer(f)
        w.writerow(data)
        convert_long.start([f.name])
        print("\nDone!")


if __name__ == "__main__":
    if args.Action.lower() == "learn":
       learn()
    elif args.Action.lower() == "create":
        for i in range(1, args.num+1):
            create(i)
