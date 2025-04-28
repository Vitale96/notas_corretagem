# parser/normalizador.py

def normalizar_linhas(df):
    """
    Recebe um DataFrame de negociações e aplica transformações para padronização.
    Retorna uma lista de dicionários normalizados.
    """
    df = df.copy()

    # 1. Substituir códigos de C/V por texto completo
    df["C/V"] = df["C/V"].map({"C": "Compra", "V": "Venda"}).fillna(df["C/V"])

    # 2. Unificar tipo e ativo (se desejar), por exemplo "PN N1 ISA ENERGIA"
    # df["Ativo"] = df["Tipo"].str.strip() + " " + df["Ativo"].str.strip()

    # 3. Remover a coluna 'Tipo', já que ela foi incorporada ao Ativo
    # df.drop(columns=["Tipo"], inplace=True)

    # 4. Garantir que os campos numéricos estejam no tipo correto
    df["Quantidade"] = df["Quantidade"].astype(int)
    df["Preço"] = df["Preço"].astype(float)
    df["Valor"] = df["Valor"].astype(float)

    # 5. (Opcional) Remover colunas não utilizadas
    df.drop(columns=["Prazo", "Obs (*)"], inplace=True, errors="ignore")

    # 6. Reordenar colunas, se desejar
    colunas_ordenadas = ["Negociação", "C/V", "Quantidade", "Preço", "Valor", "D/C", "Ativo", "Tipo","Data","Corretora"]
    df = df[colunas_ordenadas]

    # Retornar como lista de dicionários
    return df.to_dict(orient="records")


# Teste manual
if __name__ == "__main__":
    import pandas as pd
    from extrator_tabela import extrair_linhas_negociadas

    texto = """
    Bovespa
    FRA
    C
    10
    33,28
    332,80
    D
    UNT     N2
    TAESA
    """
    df = extrair_linhas_negociadas(texto)
    normalizados = normalizar_linhas(df)
    for linha in normalizados:
        print(linha)
