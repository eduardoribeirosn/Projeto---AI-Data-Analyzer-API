from io import StringIO

from flask import Flask, request
import pandas as pd

from pandas import DataFrame


arquivo = {
  "data": "nome,idade\nAna,20\nJoão,30"
}

df = pd.DataFrame(arquivo)

print(df.columns["20"])