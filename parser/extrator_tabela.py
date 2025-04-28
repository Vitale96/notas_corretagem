import pandas as pd
import re

def extrair_linhas_negociadas(texto, marcador_inicial="Bovespa", remover_coluna_bolsa=True):
    linhas = [l.strip() for l in texto.splitlines() if l.strip() and not re.match(r".*\[INFO\].*:.*", l, flags=re.DOTALL)]
    
    dados = []
    i = 0
    if linhas[1] == "Q":
        while i < len(linhas)-2:
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
                    data = linhas[-2].replace('Data: ', '')
                    corretora = linhas[-1].replace('Corretora: ', '')

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
                                    "Obs (*)": None,
                                    "Data": data,
                                    "Corretora": corretora
                                })
                    i += 9
                except Exception as e:
                    print(f"[!] Erro ao processar bloco iniciando em linha {i}: {e}")
                    i += 1
            else:
                i += 1
    else:
        while i < len(linhas)-2:
            if linhas[i] == "1-BOVESPA":
                try:
                    bolsa = linhas[i]
                    negociacao = linhas[i+2]
                    cv = linhas[i+1]
                    
                    quantidade = int(linhas[i+5])
                    preco = float(linhas[i+6].replace('.', '').replace(',', '.'))
                    valor = float(linhas[i+7].replace('.', '').replace(',', '.'))
                    dc = linhas[i+8]
                    tipo = linhas[i+4]
                    ativo = linhas[i+3]
                    data = linhas[-2].replace('Data: ', '')
                    corretora = linhas[-1].replace('Corretora: ', '')

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
                                    "Obs (*)": None,
                                    "Data": data,
                                    "Corretora": corretora
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

    df_negociacoes = extrair_linhas_negociadas(texto)
    print(df_negociacoes)


    texto = r"""
    [INFO] Processando: dados\Nota_corretagem_31-10-2022.pdf
    [INFO] Data detectada: 31/10/2022
    [INFO] Corretora detectada: INTER DTVM
    Negócios realizados
    Q
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
    20
    39,20
    784,00
    D
    UNT     N2
    TAESA
    Bovespa
    FRA
    C
    5
    39,20
    196,00
    D
    UNT     N2
    TAESA
    Bovespa
    FRA
    C
    1
    39,20
    39,20
    D
    UNT     N2
    TAESA

    ---
    Data: 31/10/2022
    Corretora: INTER DTVM
    """

    df_negociacoes = extrair_linhas_negociadas(texto)
    print(df_negociacoes)
