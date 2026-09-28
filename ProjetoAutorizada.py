from pathlib import Path

import pandas as pd


PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_EXCEL = PASTA_PROJETO / "Resources x Cities para Dispatch.xlsx"


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


if __name__ == "__main__":
    df = carregar_base()