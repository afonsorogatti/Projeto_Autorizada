from pathlib import Path
import pandas as pd
from flask import Flask, render_template, request
import sys
import webbrowser

if getattr(sys, "frozen", False):
    PASTA_PROJETO = Path(sys.executable).resolve().parent
else:
    PASTA_PROJETO = Path(__file__).resolve().parent


ARQUIVO_EXCEL = PASTA_PROJETO / "Resources x Cities para Dispatch.xlsx"


app = Flask(__name__)


def carregar_base():
    df = pd.read_excel(ARQUIVO_EXCEL)

    print("Base carregada com sucesso!")
    print(f"Quantidade de registros: {len(df)}")
    print(f"Colunas encontradas: {list(df.columns)}")

    return df


def pesquisar_cidade(df, cidade, estado):
    cidade = cidade.strip().casefold()
    estado = estado.strip().casefold()

    resultado = df[
        (df["City"].str.strip().str.casefold() == cidade)
        & (df["State"].str.strip().str.casefold() == estado)
    ]

    return resultado


def analisar_dispatch(registro):
    observacao = registro["Observação"]

    if pd.isna(observacao) or str(observacao).strip() == "":
        return {
            "tipo": "AUTOMATIC DISPATCH",
            "supplier": registro["Supplier"],
            "ppl_supplier": registro["PPL Supplier"],
        }

    return {
        "tipo": "MANUAL DISPATCH",
        "supplier": None,
        "ppl_supplier": None,
    }


df = carregar_base()


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None

    if request.method == "POST":
        cidade = request.form["cidade"]
        estado = request.form["estado"]

        pesquisa = pesquisar_cidade(df, cidade, estado)

        if pesquisa.empty:
            resultado = {
                "tipo": "CIDADE NÃO ENCONTRADA. VERIFIQUE SE FOI DIGITADA CORRETAMENTE OU SE O ESTADO SELECIONADO É O CORRETO.",
                "supplier": None,
                "ppl_supplier": None,
            }
        else:
            registro = pesquisa.iloc[0]
            resultado = analisar_dispatch(registro)

    return render_template(
        "index.html",
        resultado=resultado
    )


if __name__ == "__main__":
    import threading
    import webbrowser

    threading.Timer(
        1.5,
        lambda: webbrowser.open("http://127.0.0.1:5000")
    ).start()

    app.run(debug=False)