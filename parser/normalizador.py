import pandas as pd
import re

MAPEAMENTO_TICKERS = {
    ("BRASIL", "ON"): "BBAS3",
    ("BRADESCO", "ON"): "BBDC3",
    ("TAESA", "UNT"): "TAEE11",
    ("BBSEGURIDADE", "ON"): "BBSE3",
    ("ISA ENERGIA", "PN"): "ISAE4",
    ("TRAN PAULIST", "PN"): "ISAE4",
    ("SANTANDER BR", "ON"): "SANB3",
    ("SANTANDER BR", "PN"): "SANB4",
    ("WIZ CO", "ON"): "WIZC3",
    ("WIZ S.A.", "ON"): "WIZC3",
    ("AES BRASIL", "ON"): "AESB3",
    ("GETNET BR", "ON"): "GETT3",
    ("GETNET BR", "PN"): "GETT4",
    ("COPASA", "ON"): "CSMG3",
    ("TELEF BRASIL", "ON"): "VIVT3",
    ("ISAE4", "PN"): "ISAE4",
    ("BBAS3F", "ON"): "BBAS3",
    ("BBDC3F", "ON"): "BBDC3",
}

def normalizar_tipo(tipo: str) -> str:
    tipo = tipo.strip().upper()
    if tipo.startswith("UNT"):
        return "UNT"
    elif tipo.startswith("ON"):
        return "ON"
    elif tipo.startswith("PN"):
        return "PN"
    return tipo

def obter_ticker(ativo: str, tipo: str) -> str:
    ativo_normalizado = ativo.strip().upper()
    tipo_normalizado = tipo.strip().upper()
    return MAPEAMENTO_TICKERS.get((ativo_normalizado, tipo_normalizado), f"{ativo_normalizado}")

def normalizar_linhas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Normalizar o campo "Tipo"
    df["Tipo"] = df["Tipo"].apply(normalizar_tipo)

    # Criar coluna Ticker a partir de Ativo + Tipo
    df["Ticker"] = df.apply(lambda row: obter_ticker(row["Ativo"], row["Tipo"]), axis=1)
    
    # Garantir que os campos numéricos estejam no tipo correto
    df["Quantidade"] = df["Quantidade"].astype(int)
    df["Preço"] = df["Preço"].astype(float)
    df["Valor"] = df["Valor"].astype(float)

    # 4. Remover colunas não utilizadas
    df.drop(columns=["Prazo", "Obs (*)"], inplace=True, errors="ignore")

    # 5. Reordenar colunas
    colunas_ordenadas = ["C/V", "Quantidade", "Preço", "Valor", "Ticker", "Data", "Corretora"]
    df = df[colunas_ordenadas]

    return df.to_dict(orient="records")



# Teste manual
if __name__ == "__main__":
    import pandas as pd
    from extrator_tabela import extrair_linhas_negociadas

    texto = r"""
        [INFO] Processando: dados\nota-de-corretagem-androidx.lifecycle.MutableLiveData@2dda0ab (1).pdf
        [INFO] Data detectada: 10/03/2025
        [INFO] Corretora detectada: BTG
        Negócios realizados
        Q Negociação
        C/V
        Tipo Mercado
        Prazo
        Especificação do título
        Obs. (*)
        Quantidade
        Preço / Ajuste
        Valor Operação / Ajuste
        D/C
        1-BOVESPA
        C
        VISTA
        BBAS3
        ON
        100
        27,77
        2.777,00
        D
        1-BOVESPA
        C
        VISTA
        ISAE4
        PN
        100
        23,59
        2.359,00
        D

        --- 
        Data: 10/03/2025
        Corretora: BTG
    """

    df = extrair_linhas_negociadas(texto)
    normalizados = normalizar_linhas(df)
    for linha in normalizados:
        print(linha)
