# CP468 AI Final Project
 
 ## Intro
 The goal of this project was to create an AI which could generate human-like mouse trajectories in 3D space.
 
 The model used to accomplish this goal is an autoencoder. It is defined in cnnModel.py with the keras library.
 
 ## Data and Data Cleaning
 The original data is in the OriginalData folder. All CSV files in the OriginalData folder follow the same format:
 
 Timestamp, Rotational angle of the player at the time (pitch and yaw), Angle to the target(pitch and yaw), if the player fired, if they hit the target on a fire
 
 ### Data Cleaning
 The process of data cleaning was divided into 7 main steps, with the name of the file that does the operation at the beginning:
  1. (ODataGather.py) Gathering the data into one CSV
  2. (AngleDeltaTransform.py) Calculate the deltas in the angles (Difference in pitch with respect to time, and difference in yaw with respect to time)
  3. (ExtractMetrics.py) Extract metrics/information about the dataset. The important list that is generated here is sequencesPerTrajectory.csv. This is a list of how many points there are in every trajectory
  4. (DropFired.py) Remove/Drop all rows which have "Fired = TRUE". These are the markers for when a trajectory has eneded and the next one starts
  5. (ConstructTrajectoryTables.py) Extract every trajectory from droppedFires.csv and flatten it out into one row. Every row represents one trajectory. This is output to trajectoryTable.csv
  6. (GenerateInputOutput.py) Separate the trajectories into input training, input testing, output training, and output testing datasets
  7. (cnnModel.py) Take the flattened data and turn it into an N x 64 x 2 tensor. N is the number of rows/trajectories
