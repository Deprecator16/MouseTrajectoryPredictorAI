import pandas as pd

df = pd.read_csv("Intermediates/deltaTransformed.csv")

indicesToRemove = df[df["Fired"] == True].index
df.drop(indicesToRemove, inplace=True)
df.drop(columns=["Fired", "HitTarget"], inplace=True)
df.to_csv("Intermediates/droppedFires.csv", index=False)
