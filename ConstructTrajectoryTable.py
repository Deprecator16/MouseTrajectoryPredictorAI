import pandas as pd

df = pd.read_csv("Intermediates/droppedFires.csv")

tableColumns = ["Start Time", "End Time", "TargetRotX", "TargetRotY"]
for i in range(64):
    tableColumns.append("PlayerRotX" + str(i))
    tableColumns.append("PlayerRotY" + str(i))

chunkSizes = pd.read_csv("Intermediates/sequencesPerTrajectory.csv")

dfAppendList = []
chunkIndex = 0
for index, _ in chunkSizes.iterrows():
    size = chunkSizes.iat[index, 0]
    chunk = df.iloc[chunkIndex:chunkIndex + size]
    chunkIndex += size
    
    newFrameList = []
    newFrameList.append(chunk.iloc[0, 0])
    newFrameList.append(chunk.iloc[size - 1, 0])
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

appendingDF = pd.DataFrame(dfAppendList, columns=tableColumns)
appendingDF.to_csv("Intermediates/trajectoryTable.csv", index=False)