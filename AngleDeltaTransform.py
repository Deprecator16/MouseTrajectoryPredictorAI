from cmath import nan
from numpy import NaN, isnan
import pandas as pd

df = pd.read_csv("Intermediates/gathered.csv")
numRows = len(df.index)

zeroAngle = None
targetAngle = None
for index, row in df.iterrows():
    if row.iat[5] == True:
        if isnan(row.iat[3]):
            zeroAngle = (row.iat[1], row.iat[2])
            df.iat[index, 1] = 0.0
            df.iat[index, 2] = 0.0
            targetAngle = (df.iat[index + 1, 3], df.iat[index + 1, 4])
        else:
            nextZeroAngle = (row.iat[1], row.iat[2])
            df.iat[index, 1] -= zeroAngle[0]
            df.iat[index, 2] -= zeroAngle[1]
            df.iat[index, 3] = targetAngle[0]
            df.iat[index, 4] = targetAngle[1]
            zeroAngle = nextZeroAngle

            if index + 1 < numRows and not isnan(row.iat[3]):
                targetAngle = (df.iat[index + 1, 3], df.iat[index + 1, 4])
    else:
        nextZeroAngle = (row.iat[1], row.iat[2])
        df.iat[index, 1] -= zeroAngle[0]
        df.iat[index, 2] -= zeroAngle[1]
        df.iat[index, 3] = targetAngle[0]
        df.iat[index, 4] = targetAngle[1]
        zeroAngle = nextZeroAngle

df.to_csv('Intermediates/deltaTransformed.csv', index=False)
      