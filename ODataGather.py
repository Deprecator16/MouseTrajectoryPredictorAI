import os
import pandas as pd
import numpy as np

file_list = []
fl = os.listdir("OriginalData")

for file in fl:
  if file.endswith('.csv'):
    file_list.append(file)

data_frames = []
for filename in file_list:
  pathString = 'OriginalData\\' + filename
  fr = pd.read_csv(pathString)
  data_frames.append(fr)

gatheredFrame = None
for frame in data_frames:
  gatheredFrame = pd.concat(data_frames)

gatheredFrame.to_csv('Intermediates/gathered.csv', index=False)
