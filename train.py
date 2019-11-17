#!/usr/bin/env python

import numpy as np
from keras.layers import LSTM, Input
from keras.models import Model
from keras.utils.np_utils import to_categorical

from PointerLSTM import PointerLSTM
from data_reader import get_data

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

#


path = "data/data.ptr"

split_at = 1100
batch_size = 64

hidden_size = 64
weights_file = 'model_weights.hdf5'

x, y = get_data(path)

y = y-1

YY = []
i = 0
for y_ in y:
    cat = to_categorical(y_)
    if (cat.shape==(200,201)):
        print(cat.shape)
    YY.append(cat)
    i += 1
YY = np.asarray(YY)

x_train = x[:split_at]
x_test = x[split_at:]

y_test = y[split_at:]
YY_train = YY[:split_at]
YY_test = YY[split_at:]

print(YY.shape)

print("building model...")
main_input = Input(shape=(200, 60), name='main_input')

encoder = LSTM(units=hidden_size, return_sequences=True, name="encoder")(main_input)
print(encoder)
decoder = PointerLSTM(hidden_size, units=hidden_size, name="decoder")(encoder)

model = Model(inputs=main_input, outputs=decoder)
"""
print("loading weights from {}...".format(weights_file))
try:
    model.load_weights(weights_file + "5")
except IOError:
    print("no weights file, starting anew.")
"""
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

print('training and saving model weights each epoch...')

validation_data = (x_test, YY_test)

epoch_counter = 0

history = model.fit(x_train, YY_train, epochs=10, batch_size=batch_size,
                    validation_data=validation_data)

p = model.predict(x_test)

for y_, p_ in list(zip(y_test, p))[:5]:
    print("epoch_counter: ", epoch_counter)
    print("y_test:", y_)
    print("p:     ", p_.argmax(axis=1))
    print()

model.save(weights_file)