import fitz  # PyMuPDF
from pathlib import Path
import re
import logging
from typing import Optional

# Configurar o logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

def ler_texto_pdf(caminho_pdf: str) -> str:
    """
    Lê todas as páginas de um PDF e retorna o conteúdo concatenado em uma única string.
    
    Args:
        caminho_pdf (str): Caminho para o arquivo PDF.
    
    Returns:
        str: Texto completo do PDF.
    """
    caminho = Path(caminho_pdf)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_pdf}")

    texto = []
    try:
        with fitz.open(caminho_pdf) as doc:
            for pagina in doc:
                texto.append(pagina.get_text())
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o PDF: {e}")

    return "\n".join(texto)


def extrair_trecho_negocios(texto: str) -> Optional[str]:
    """
    Extrai o trecho de negócios realizados do texto do PDF.
    
    Args:
        texto (str): Texto completo do PDF.
    
    Returns:
        Optional[str]: Trecho de negócios encontrados ou None se não encontrado.
    """
    padrao = (
        r'Negócios realizados'                  # Ponto de início
        r'(.*?)'                                 # Captura tudo de forma preguiçosa
        r'(?=Resumo dos Negócios|DOCUMENTO HÁBIL PARA IMPOSTO DE RENDA)'  # Ponto de parada (lookahead)
    )

    match = re.search(padrao, texto, flags=re.S | re.I)
    if match:
        return match.group(0).strip()
    else:
        return None


def detectar_data_corretora(texto: str) -> tuple[Optional[str], Optional[str]]:
    """
    Detecta a data e o nome da corretora no texto do PDF.

    Args:
        texto (str): Texto completo do PDF.

    Returns:
        tuple: (data encontrada, corretora encontrada) ou (None, None) se não encontrado.
    """
    # Procurar data no formato dd/mm/yyyy
    match_data = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', texto)
    data = match_data.group(1) if match_data else None

    # Procurar corretora por palavras-chave conhecidas
    corretoras = ['INTER DTVM', 'BTG', 'XP INVESTIMENTOS', 'RICO INVESTIMENTOS', 'CLEAR CORRETORA', 'NU INVEST', 'MODAL DTVM']
    corretora = None
    for nome in corretoras:
        if nome.lower() in texto.lower():
            corretora = nome
            break

    return data, corretora


def extrair_informacoes(caminho_pdf: str) -> Optional[str]:
    """
    Função principal que extrai o trecho de negócios realizados e anexa a data e a corretora.
    
    Args:
        caminho_pdf (str): Caminho para o arquivo PDF.
    
    Returns:
        Optional[str]: Trecho formatado com negócios, data e corretora ou None.
    """
    logging.info(f"Processando: {caminho_pdf}")
    
    try:
        texto_pdf = ler_texto_pdf(caminho_pdf)
    except Exception as e:
        logging.error(str(e))
        return None

    trecho_negocios = extrair_trecho_negocios(texto_pdf)
    if not trecho_negocios:
        logging.warning("Trecho de negócios não encontrado.")
        return None

    data, corretora = detectar_data_corretora(texto_pdf)

    logging.info(f"Data detectada: {data if data else 'Não encontrada'}")
    logging.info(f"Corretora detectada: {corretora if corretora else 'Não encontrada'}")

    # Anexar data e corretora no final
    informacoes_adicionais = "\n\n---\n"
    if data:
        informacoes_adicionais += f"Data: {data}\n"
    if corretora:
        informacoes_adicionais += f"Corretora: {corretora}\n"

    return trecho_negocios + informacoes_adicionais

# Exemplo de uso:
if __name__ == "__main__":
    caminho = r"dados\nota-de-corretagem-androidx.lifecycle.MutableLiveData@2dda0ab (1).pdf"
    texto = extrair_informacoes(caminho)
    print(texto)
    caminho = r"dados\Nota_corretagem_31-10-2022.pdf"
    texto = extrair_informacoes(caminho)
    print(texto)
