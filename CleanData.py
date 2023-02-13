import os
import sys
import numpy as np
import pandas as pd

#----------------------------------------
# Parameters for what files will be output from running this script
#----------------------------------------
trainingSplit = 0.6         # Percentage of data which will be used for training. The rest will go to testing
outputIntermediates = False # Output intermediate stages into files
outputMetrics = False       # Output metrics on data

####################
# Gather all raw mouse data into one dataframe
####################
gatheredFrame = pd.DataFrame()
for file in os.listdir("OriginalData"):
  if file.endswith('.csv'):
    gatheredFrame = pd.concat([gatheredFrame, pd.read_csv("OriginalData\\" + file)], ignore_index=True)

if outputIntermediates:
    gatheredFrame.to_csv('Intermediates/gathered.csv', index=False)

####################
# Calculate the deltas in the angles (Difference in pitch with respect to time, and difference in yaw with respect to time)
####################
numRows = len(gatheredFrame.index)
zeroAngle = None
targetAngle = None
for index, row in gatheredFrame.iterrows():
    if row.iat[5] == True:
        if np.isnan(row.iat[3]):
            zeroAngle = (row.iat[1], row.iat[2])
            gatheredFrame.iat[index, 1] = 0.0
            gatheredFrame.iat[index, 2] = 0.0
            targetAngle = (gatheredFrame.iat[index + 1, 3] - zeroAngle[0], gatheredFrame.iat[index + 1, 4] - zeroAngle[1])
        else:
            nextZeroAngle = (row.iat[1], row.iat[2])
            gatheredFrame.iat[index, 1] -= zeroAngle[0]
            gatheredFrame.iat[index, 2] -= zeroAngle[1]
            gatheredFrame.iat[index, 3] = targetAngle[0]
            gatheredFrame.iat[index, 4] = targetAngle[1]
            zeroAngle = nextZeroAngle

            if index + 1 < numRows and not np.isnan(row.iat[3]):
                targetAngle = (gatheredFrame.iat[index + 1, 3] - zeroAngle[0], gatheredFrame.iat[index + 1, 4] - zeroAngle[1])
    else:
        nextZeroAngle = (row.iat[1], row.iat[2])
        gatheredFrame.iat[index, 1] -= zeroAngle[0]
        gatheredFrame.iat[index, 2] -= zeroAngle[1]
        gatheredFrame.iat[index, 3] = targetAngle[0]
        gatheredFrame.iat[index, 4] = targetAngle[1]
        zeroAngle = nextZeroAngle

if outputIntermediates:
    gatheredFrame.to_csv('Intermediates/deltaTransformed.csv', index=False)

####################
# Extract metrics/information about the dataset. The important list that is generated here is sequencesPerTrajectory.csv.
# This is a list of how many points there are in every trajectory
####################
min = sys.maxsize
max = 0
trajectoryIndex = -1
sequencesPerTrajectory = []
for index, row in gatheredFrame.iterrows():
    if row.iat[5] == True:
        if np.isnan(row.iat[3]):
            if trajectoryIndex >= 0:
                if sequencesPerTrajectory[trajectoryIndex] > max:
                    max = sequencesPerTrajectory[trajectoryIndex]
                if sequencesPerTrajectory[trajectoryIndex] < min:
                    min = sequencesPerTrajectory[trajectoryIndex]
            trajectoryIndex += 1
            sequencesPerTrajectory.append(0)
        elif index + 1 < numRows and not np.isnan(gatheredFrame.iat[index + 1, 3]):
            if trajectoryIndex >= 0 and trajectoryIndex < numRows:
                if sequencesPerTrajectory[trajectoryIndex] > max:
                    max = sequencesPerTrajectory[trajectoryIndex]
                if sequencesPerTrajectory[trajectoryIndex] < min:
                    min = sequencesPerTrajectory[trajectoryIndex]
            trajectoryIndex += 1
            sequencesPerTrajectory.append(0)
    else:
        sequencesPerTrajectory[trajectoryIndex] += 1
        
sequencesTotal = sum(sequencesPerTrajectory)
trajectoryAverage = sequencesTotal / (trajectoryIndex + 1)

if outputMetrics:
    with open("Intermediates/metrics.txt", "a") as fw:
        fw.truncate(0)
        fw.write("Total trajectories: {}\n".format(trajectoryIndex + 1))
        fw.write("Total sequences: {}\n".format(sequencesTotal))
        fw.write("Average sequences per trajectory: {}\n".format(trajectoryAverage))
        fw.write("Max sequences in trajectory: {}\n".format(max))
        fw.write("Min sequences in trajectory: {}\n\n".format(min))

        underSeq = [10, 32, 48, 50, 65, 75, 100, 125, 150, max]
        for i in range(len(underSeq)):
            under = sum(1 for e in sequencesPerTrajectory if e < underSeq[i])
            fw.write("Trajectories under {} sequences: {}\n".format("max" if i == len(underSeq) - 1 else underSeq[i], under))

with open("Intermediates/sequencesPerTrajectory.csv", "a") as st:
    st.truncate(0)
    st.write("TrajectorySize\n")
    for e in sequencesPerTrajectory:
        st.write("{}\n".format(e))

####################
# Remove/Drop all rows which have "Fired = TRUE". These are the markers for when a trajectory has eneded and the next one starts
####################
indicesToRemove = gatheredFrame[gatheredFrame["Fired"] == True].index
gatheredFrame.drop(indicesToRemove, inplace=True)
gatheredFrame.drop(columns=["Fired", "HitTarget"], inplace=True)

if outputIntermediates:
    gatheredFrame.to_csv("Intermediates/droppedFires.csv", index=False)

####################
# Extract every trajectory from droppedFires.csv and flatten it out into one row. Every row represents one trajectory.
# This is output to trajectoryTable.csv
####################
tableColumns = ["Start Time", "End Time", "SequenceSize", "TargetRotX", "TargetRotY"]
for i in range(64):
    tableColumns.append("PlayerRotX" + str(i))
    tableColumns.append("PlayerRotY" + str(i))

chunkSizes = pd.read_csv("Intermediates/sequencesPerTrajectory.csv")

dfAppendList = []
chunkIndex = 0
for index, _ in chunkSizes.iterrows():
    size = chunkSizes.iat[index, 0]
    chunk = gatheredFrame.iloc[chunkIndex:chunkIndex + size]
    chunkIndex += size

    newFrameList = []
    newFrameList.append(chunk.iloc[0, 0])
    newFrameList.append(chunk.iloc[size - 1, 0])
    newFrameList.append(size)
    newFrameList.append(chunk.iloc[0, 3])
    newFrameList.append(chunk.iloc[0, 4])

    for i in range(64):
        if i < size:
            newFrameList.append(chunk.iloc[i, 1])
            newFrameList.append(chunk.iloc[i, 2])
        else:
            newFrameList.append(0)
            newFrameList.append(0)
    dfAppendList.append(newFrameList)

outputData = pd.DataFrame(dfAppendList, columns=tableColumns)
if outputIntermediates:
    outputData.to_csv("Intermediates/trajectoryTable.csv", index=False)

####################
# Separate the trajectories into input training, input testing, output training, and output testing datasets
####################
outputData.drop(columns=["Start Time", "End Time", "SequenceSize"], inplace=True)

inputData = outputData[outputData.columns[0:2]].copy()
if outputIntermediates:
    inputData.to_csv("Intermediates/inputData.csv", index=False)

outputData.drop(columns=["TargetRotX", "TargetRotY"], inplace=True)
if outputIntermediates:
    outputData.to_csv("Intermediates/outputData.csv", index=False)

numRows = len(outputData.index)
splitPoint = int(numRows * trainingSplit)
inputTrainingData = inputData[:splitPoint].copy()
inputTestingData = inputData[splitPoint:].copy()
outputTrainingData = outputData[:splitPoint].copy()
outputTestingData = outputData[splitPoint:].copy()

inputTrainingData.to_csv("CleanedData/inputTrainingData.csv", index=False)
inputTestingData.to_csv("CleanedData/inputTestingData.csv", index=False)
outputTrainingData.to_csv("CleanedData/outputTrainingData.csv", index=False)
outputTestingData.to_csv("CleanedData/outputTestingData.csv", index=False)