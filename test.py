from io import StringIO

from flask import Flask, request
import pandas as pd

string = "nome,idade\nAna,20\nJoão,30"
file_memory_data = StringIO(string)
df = pd.read_csv(file_memory_data)

print(df.columns.tolist())
for item_type in df.dtypes:
  print(item_type)

print(type(file_memory_data))
print(type("aa"))

