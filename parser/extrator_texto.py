import fitz  # PyMuPDF
from pathlib import Path
import re

def extrair_texto_pdf(caminho_pdf: str) -> str:
    """
    Extrai todo o texto de um arquivo PDF usando PyMuPDF (fitz).
    Retorna uma string com todo o conteúdo concatenado.
    """
    caminho = Path(caminho_pdf)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_pdf}")

    texto = []
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto.append(pagina.get_text())
            texto_completo = "\n".join(texto)

            # Buscar o trecho entre "Acionista" e "INTER DTVM LTDA."
            match = re.search(r"(Q\n(?P<foo>Negociação.*?)DOCUMENTO HÁBI\.*)", texto_completo, flags=re.DOTALL)

            # Verifica se encontrou
            if match:
                trecho_desejado = match.group(2)
                print(trecho_desejado)
            else:
                trecho_desejado = None
                print("❌ Trecho não encontrado.")

    return trecho_desejado

# Exemplo de uso:
if __name__ == "__main__":
    caminho = r"dados\11-03-2025_10548190_2025041715011522569500.pdf"
    texto = extrair_texto_pdf(caminho)
    print(texto[:1000])  # Mostra os primeiros 1000 caracteres para inspeção
