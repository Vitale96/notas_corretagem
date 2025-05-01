from parser.extrator_texto import extrair_informacoes
from parser.extrator_tabela import extrair_linhas_negociadas
from parser.normalizador import normalizar_linhas

from pathlib import Path
import csv
import os
import sqlite3
import pandas as pd
# import xlsxwriter

def carregar_notas_da_pasta(pasta):
    return [
        os.path.abspath(os.path.join(pasta, f)).replace("\\", "/")
        for f in os.listdir(pasta)
        if f.endswith(".pdf")
    ]

def criar_tabela(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS negociacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT,
            ticker TEXT,
            quantidade INTEGER,
            preco_unitario REAL,
            valor_total REAL,
            corretora TEXT,
            origem_arquivo TEXT
        )
    """)
    conn.commit()

def salvar_em_sqlite(dados, conn):
    for linha in dados:
        try:
            conn.execute("""
                INSERT INTO negociacoes (
                    data, ticker, quantidade, preco_unitario,
                    valor_total, corretora, origem_arquivo
                ) VALUES (
                    :data, :ticker, :quantidade, :preco_unitario,
                    :valor_total, :corretora, :origem_arquivo
                )
            """, linha)
        except Exception as e:
            print(f"Erro ao inserir linha no banco: {linha}")
            print(e)
    conn.commit()

pasta = r"C:\Users\vital\Documents\programas\notas_corretagem\dados"
saida_csv = "output/negociacoes.csv"
saida_xlsx = "output/negociacoes.xlsx"
saida_sqlite = "output/negociacoes.db"

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect(saida_sqlite)
criar_tabela(conn)

todas_linhas = []

for arq in carregar_notas_da_pasta(pasta):
    caminho_pdf = Path(arq)
    texto = extrair_informacoes(caminho_pdf)
    linhas_raw = extrair_linhas_negociadas(texto)
    linhas = normalizar_linhas(linhas_raw)

    # Mapeia os campos para o formato do banco
    linhas_sqlite = [
        {
            "data": l["Data"],
            "ticker": l["Ticker"],
            "quantidade": l["Quantidade"],
            "preco_unitario": l["Preço"],
            "valor_total": l["Valor"],
            "corretora": l["Corretora"],
            "origem_arquivo": caminho_pdf.name
        }
        for l in linhas
    ]

    salvar_em_sqlite(linhas_sqlite, conn)
    todas_linhas.extend(linhas_sqlite)

# Exporta para CSV
with open(saida_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=todas_linhas[0].keys())
    writer.writeheader()
    writer.writerows(todas_linhas)

# Exporta para Excel
df = pd.DataFrame(todas_linhas)
df.drop_duplicates(inplace=True)

# Converte a coluna 'data' para datetime
df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")

# Exporta para Excel com formatação correta de datas
with pd.ExcelWriter(saida_xlsx, engine="openpyxl", datetime_format="yyyy-mm-dd") as writer:
    df.to_excel(writer, index=False)



print(f"✅ Exportações concluídas: {saida_csv}, {saida_xlsx}, {saida_sqlite}")
