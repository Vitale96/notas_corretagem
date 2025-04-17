import pandas as pd
import re

def extrair_linhas_negociadas(texto, marcador_inicial="Bovespa", remover_coluna_bolsa=True):
    linhas = [l.strip() for l in texto.splitlines() if l.strip() and not re.match(r"^[A-Z][a-z]+.*:", l)]
    
    dados = []
    i = 0
    while i < len(linhas):
        if linhas[i] == marcador_inicial:
            try:
                bolsa = linhas[i]
                negociacao = linhas[i+1]
                cv = linhas[i+2]
                
                quantidade = int(linhas[i+3])
                preco = float(linhas[i+4].replace('.', '').replace(',', '.'))
                valor = float(linhas[i+5].replace('.', '').replace(',', '.'))
                dc = linhas[i+6]
                tipo = linhas[i+7]
                ativo = linhas[i+8]

                # Verificação de consistência (com margem de tolerância)
                valor_calc = round(quantidade * preco, 2)
                if abs(valor - valor_calc) > 0.01:
                    print(f"[!] Divergência detectada em linha {i}: {quantidade} * {preco:.2f} = {valor_calc:.2f}, mas valor informado é {valor:.2f}")

                dados.append({
                    "Bolsa": bolsa,
                    "Negociação": negociacao,
                    "C/V": cv,
                    "Quantidade": quantidade,
                    "Preço": preco,
                    "Valor": valor,
                    "D/C": dc,
                    "Tipo": tipo,
                    "Ativo": ativo,
                    "Prazo": None,
                    "Obs (*)": None
                })
                i += 9
            except Exception as e:
                print(f"[!] Erro ao processar bloco iniciando em linha {i}: {e}")
                i += 1
        else:
            i += 1

    df = pd.DataFrame(dados)

    if remover_coluna_bolsa and "Bolsa" in df.columns:
        df.drop(columns=["Bolsa"], inplace=True)

    return df


if __name__ == "__main__":

    texto = """
    Negociação
    C/V
    Tipo mercado
    Prazo
    Especificação do titulo
    Obs (*)
    Quantidade
    Preço/Ajuste
    Valor
    D/C
    Bovespa
    FRA
    C
    10
    33,28
    332,80
    D
    UNT     N2
    TAESA
    Bovespa
    FRA
    C
    40
    23,61
    944,40
    D
    PN      N1
    ISA ENERGIA
    Bovespa
    VIS
    C
    100
    23,61
    2.361,00
    D
    PN      N1
    ISA ENERGIA
    """

    df_negociacoes = extrair_linhas_negociadas(texto)
    print(df_negociacoes)
