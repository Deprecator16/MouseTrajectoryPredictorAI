import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Conv1D, GlobalAveragePooling1D, Conv1DTranspose, Reshape
from keras.utils import np_utils

inTraining = pd.read_csv("CleanedData/inputTrainingData.csv")
inTesting = pd.read_csv("CleanedData/inputTestingData.csv")
outTraining = pd.read_csv("CleanedData/outputTrainingData.csv")
outTesting = pd.read_csv("CleanedData/outputTestingData.csv")

inputTraining = np.zeros((len(inTraining.index), 64, 2))
for index, row in inTraining.iterrows():
    rotX = row.iat[0]
    rotY = row.iat[1]
    dX = rotX / 64
    dY = rotY / 64
    for i in range(64):
        inputTraining[index, i, 0] = dX * (i + 1)
        inputTraining[index, i, 1] = dY * (i + 1)

inputTesting = np.zeros((len(inTesting.index), 64, 2))
for index, row in inTesting.iterrows():
    rotX = row.iat[0]
    rotY = row.iat[1]
    dX = rotX / 64
    dY = rotY / 64
    for i in range(64):
        inputTesting[index, i, 0] = dX * (i + 1)
        inputTesting[index, i, 1] = dY * (i + 1)

outputTraining = np.zeros((len(outTraining.index), 64, 2))
for index, row in outTraining.iterrows():
    allX = np.array(row.iloc[::2].copy())
    allY = np.array(row.iloc[1::2])
    conc = np.stack([allX,allY]).transpose().copy()
    outputTraining[index] = conc

outputTesting = np.zeros((len(outTesting.index), 64, 2))
for index, row in outTesting.iterrows():
    allX = np.array(row.iloc[::2].copy())
    allY = np.array(row.iloc[1::2])
    conc = np.stack([allX,allY]).transpose().copy()
    outputTesting[index] = conc

model = Sequential()
model.add(Conv1D(filters=64, kernel_size=8, input_shape=(64,2), activation="relu"))
model.add(Conv1D(filters=128, kernel_size=5, activation="relu"))
model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
model.add(GlobalAveragePooling1D())
model.add(Reshape((64,1)))
model.add(Conv1D(filters=64, kernel_size=3, activation="relu"))
model.add(Conv1D(filters=128, kernel_size=5, activation="relu"))
model.add(Conv1D(filters=2, kernel_size=8))

print(model.output_shape)

# model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse', 'mae'])
# model.fit(inputTraining, outputTraining, batch_size=32, epochs=100, verbose=1)
# score = model.evaluate(inputTesting, outputTesting, verbose=1)
# print(score)
