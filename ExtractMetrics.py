from numpy import isnan
import sys
import pandas as pd

df = pd.read_csv("Intermediates/deltaTransformed.csv")
numRows = len(df.index)

min = sys.maxsize
max = 0
trajectoryIndex = -1
sequencesPerTrajectory = []
for index, row in df.iterrows():
    if row.iat[5] == True:
        if isnan(row.iat[3]):
            if trajectoryIndex >= 0:
                if sequencesPerTrajectory[trajectoryIndex] > max:
                    max = sequencesPerTrajectory[trajectoryIndex]
                if sequencesPerTrajectory[trajectoryIndex] < min:
                    min = sequencesPerTrajectory[trajectoryIndex]
            trajectoryIndex += 1
            sequencesPerTrajectory.append(0)
        elif index + 1 < numRows and not isnan(row.iat[3]):
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

fw = open("Intermediates/metrics.txt", "a")
fw.write("Total trajectories: {}\n".format(trajectoryIndex + 1))
fw.write("Total sequences: {}\n".format(sequencesTotal))
fw.write("Average sequences per trajectory: {}\n".format(trajectoryAverage))
fw.write("Max sequences in trajectory: {}\n".format(max))
fw.write("Min sequences in trajectory: {}\n\n".format(min))

under10 = sum(1 for e in sequencesPerTrajectory if e < 10)
under50 = sum(1 for e in sequencesPerTrajectory if e < 50)
under65 = sum(1 for e in sequencesPerTrajectory if e < 65)
under75 = sum(1 for e in sequencesPerTrajectory if e < 75)
under100 = sum(1 for e in sequencesPerTrajectory if e < 100)
under100 = sum(1 for e in sequencesPerTrajectory if e < 100)
under125 = sum(1 for e in sequencesPerTrajectory if e < 125)
under150 = sum(1 for e in sequencesPerTrajectory if e < 150)
underMax = sum(1 for e in sequencesPerTrajectory if e < max)

fw.write("Trajectories under 10 sequences: {}\n".format(under10))
fw.write("Trajectories under 50 sequences: {}\n".format(under50))
fw.write("Trajectories under 65 sequences: {}\n".format(under65))
fw.write("Trajectories under 75 sequences: {}\n".format(under75))
fw.write("Trajectories under 100 sequences: {}\n".format(under100))
fw.write("Trajectories under 125 sequences: {}\n".format(under125))
fw.write("Trajectories under 150 sequences: {}\n".format(under150))
fw.write("Trajectories under max sequences: {}\n".format(underMax))
fw.close()

st = open("Intermediates/sequencesPerTrajectory.csv", "a")
for e in sequencesPerTrajectory:
    st.write("{},\n".format(e))
st.close()
