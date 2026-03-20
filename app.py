from io import StringIO
from typing import TypedDict

from flask import Flask, request
import pandas as pd
from pandas import DataFrame
from langgraph.graph import StateGraph, END


# Criação da Class
class State(TypedDict):
    data: str
    # data_io: str
    df: DataFrame
    linhas: int
    colunas: int
    nomes_colunas: list
    tipos_colunas: list

# Criação da ligação do Flask
app = Flask(__name__)

def generate_dataframe(state : State):
    try:
        data_io_temp = StringIO(state["data"])
        df_temp = pd.read_csv(data_io_temp)
    except Exception:
        return {"df": None}
    return {"df": df_temp}

# Conditional Edge
def verify_error_df(state: State):
    if isinstance(state["df"], DataFrame):
        return "continue"
    else:
        return "erro"

def count_lines(state : State):
    return {"linhas": state["df"].shape[0]}

def count_columns(state: State):
    return {"colunas": state["df"].shape[1]}

def analyze_name_data(state : State):
    return {"nomes_colunas": state["df"].columns.tolist()}

def analyze_typed_data(state: State):
    temp_typed_columns = []
    for item_type in state["df"].dtypes:
        if item_type == "int64":
            temp_typed_columns.append("número")
        elif pd.api.types
        else:
            temp_typed_columns.append("text")
    print(temp_typed_columns)
    return {"tipos_colunas": temp_typed_columns}

# Construir Graph
def build_graph():
    # Criar o Graph
    graph = StateGraph(State)

    # Adicionar os nodes
    # graph.add_node("generate_data_io", generate_data_io)
    graph.add_node("parse_data", generate_dataframe)
    # graph.add_node("verify_error_df", verify_error_df)
    graph.add_node("count_lines", count_lines)
    graph.add_node("count_columns", count_columns)
    graph.add_node("analyze_name_data", analyze_name_data)
    graph.add_node("analyze_typed_data", analyze_typed_data)

    # Adicionar os Edges (caminhos)
    graph.set_entry_point("parse_data")
    # graph.add_edge("generate_data_io", "parse_data")
    graph.add_conditional_edges(
        "parse_data",
        verify_error_df,
        {
            "continue": "count_lines",
            "erro": END
        }
    )
    # graph.add_edge("parse_data", "count_lines")
    graph.add_edge("count_lines", "count_columns")
    graph.add_edge("count_columns", "analyze_name_data")
    graph.add_edge("analyze_name_data", "analyze_typed_data")
    graph.add_edge("analyze_typed_data", END)

    return graph.compile()

graph_compiled = build_graph()


@app.route("/analyze", methods=["POST"])
def analyze():
    content_json = request.json
    try:
        data = content_json["data"]
    except Exception:
        return {"message": "CSV não encontrado"}

    result = graph_compiled.invoke(
        {"data": data}
    )

    if not isinstance(result["df"], DataFrame):
        return {"message": "CSV inválido"}

    result_changed = {
        "linhas": result["linhas"],
        "colunas": result["colunas"],
        "nomes_colunas": result["nomes_colunas"],
        "tipos_colunas": result["tipos_colunas"],
    }

    return result_changed


if __name__ == "__main__":
    app.run(debug=True)