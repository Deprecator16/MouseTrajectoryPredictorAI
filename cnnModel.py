# GitHub repositories for this project can be found at the following links:
# Autoencoder Model: https://github.com/Deprecator16/CP468-AI-Final-Project
# Unreal Engine 5 Data Collector: https://github.com/Deprecator16/MTDataCollector

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Conv1D, GlobalAveragePooling1D, Conv1DTranspose, Reshape
from matplotlib import pyplot as plt

inTraining = pd.read_csv("CleanedData/inputTrainingData.csv")
inTesting = pd.read_csv("CleanedData/inputTestingData.csv")
outTraining = pd.read_csv("CleanedData/outputTrainingData.csv")
outTesting = pd.read_csv("CleanedData/outputTestingData.csv")

#########
# Restructure data before sending into model
########
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

########
# Start creating the model here
########

model = Sequential()
model.add(Conv1D(filters=64, kernel_size=8, input_shape=(64,2), padding='same',activation="relu"))
model.add(Conv1D(filters=128, kernel_size=5, padding='same', activation="relu"))
model.add(Conv1D(filters=64, kernel_size=3, padding='same', activation="relu"))
model.add(GlobalAveragePooling1D())
model.add(Reshape((64,1)))
model.add(Conv1DTranspose(filters=64, kernel_size=3, padding='same', activation="relu"))
model.add(Conv1DTranspose(filters=128, kernel_size=5, padding='same', activation="relu"))
model.add(Conv1DTranspose(filters=2, kernel_size=3, padding='same'))

# print(model.output_shape)

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse', 'mae'])
model.fit(inputTraining, outputTraining, batch_size=32, epochs=150, verbose=1)
score = model.evaluate(inputTesting, outputTesting, verbose=1)
predictions = model.predict(inputTesting)



# Testing Code
# pdPred0 = pd.DataFrame(predictions[0], columns=["DeltaRotX", "DeltaRotY"])
# pdPred1 = pd.DataFrame(predictions[1], columns=["DeltaRotX", "DeltaRotY"])
# pdPred2 = pd.DataFrame(predictions[2], columns=["DeltaRotX", "DeltaRotY"])
# pdPred0.to_csv("Prediction0.csv", index=False)
# pdPred1.to_csv("Prediction1.csv", index=False)
# pdPred2.to_csv("Prediction2.csv", index=False)


# Best: 1
# indexToGraph = 1
# plotShowInput = inputTesting[indexToGraph].transpose()
# plotShowOutput = outputTesting[indexToGraph].transpose()
# plotShowPrediction = predictions[indexToGraph].transpose()
# plt.plot(plotShowInput[0], 'bo-')
# plt.plot(plotShowOutput[0], 'ro-')
# plt.plot(plotShowPrediction[0], 'go-')
# plt.xlabel("Time (16.66 ms per step)")
# plt.ylabel("Delta Pitch (Degrees)")
# plt.show()