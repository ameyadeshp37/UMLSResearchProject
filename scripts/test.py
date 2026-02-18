import pandas as pd

edges = pd.read_csv("outputs/edges.csv")

print(edges.head())
print(edges["relationship"].value_counts())
print(edges.duplicated().sum())