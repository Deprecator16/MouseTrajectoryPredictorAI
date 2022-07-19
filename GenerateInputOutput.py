import pandas as pd

outputData = pd.read_csv("Intermediates/trajectoryTable.csv")
outputData.drop(columns=["Start Time", "End Time", "SequenceSize"], inplace=True)

inputData = outputData[outputData.columns[0:2]].copy()
inputData.to_csv("Intermediates/inputData.csv", index=False)

outputData.drop(columns=["TargetRotX", "TargetRotY"], inplace=True)
outputData.to_csv("Intermediates/outputData.csv", index=False)

inputTrainingData = inputData[::2].copy()
inputTestingData = inputData[1::2].copy()
outputTrainingData = outputData[::2].copy()
outputTestingData = outputData[1::2].copy()

inputTrainingData.to_csv("CleanedData/inputTrainingData.csv", index=False)
inputTestingData.to_csv("CleanedData/inputTestingData.csv", index=False)
outputTrainingData.to_csv("CleanedData/outputTrainingData.csv", index=False)
outputTestingData.to_csv("CleanedData/outputTestingData.csv", index=False)
