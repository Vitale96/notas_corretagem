# main.py
from parser.extrator_texto import extrair_texto_pdf
from parser.extrator_tabela import extrair_linhas_negociadas
from parser.normalizador import normalizar_linhas
from pathlib import Path
import csv
import os

def carregar_notas_da_pasta(pasta):
    notas = [
        os.path.abspath(os.path.join(pasta, f)).replace("\\", "/")
        for f in os.listdir(pasta)
        if f.endswith(".pdf")
    ]
    return notas

pasta = r"C:\Users\vital\Documents\programas\notas_corretagem\dados"

for arq in carregar_notas_da_pasta(pasta):
    caminho_pdf = Path(arq)
    texto = extrair_texto_pdf(caminho_pdf)
    linhas_raw = extrair_linhas_negociadas(texto)
    dados_normalizados = normalizar_linhas(linhas_raw)

    with open("output/negociacoes.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=dados_normalizados[0].keys())
        writer.writeheader()
        writer.writerows(dados_normalizados)