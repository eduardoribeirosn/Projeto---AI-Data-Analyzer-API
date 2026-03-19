from io import StringIO

from flask import Flask, request
import pandas as pd

from pandas import DataFrame

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    content_json = request.json
    data = content_json["data"]

    # Transformando CSV em DataFrame
    file_memory_data = StringIO(data)
    df = pd.read_csv(file_memory_data)

    # Validação se deu certo
    if not isinstance(df, DataFrame):
        return {"message": "CSV inválido"}

    linhas = count_lines(df)
    colunas = count_column(df)
    nameColumns = analyze_data(df)

    return {"linhas": linhas, "colunas": colunas, "nomes_colunas": nameColumns} # ...

def count_lines(file_csv : DataFrame):
    return file_csv.shape[0]
    # return (file_csv.split("\n"))

def count_column(file_csv : DataFrame):
    return file_csv.shape[1]

def analyze_data(file_csv : DataFrame):
    return file_csv.columns.tolist()


if __name__ == "__main__":
    app.run(debug=True)