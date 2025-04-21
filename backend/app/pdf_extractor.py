import os
import fitz  # PyMuPDF

# Caminho dinâmico para a pasta pdf_contexto dentro da pasta atual
pdf_folder = os.path.join(os.path.dirname(__file__), "pdf_contexto")

# Função para extrair texto de um único PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

# Função para extrair texto de todos os PDFs na pasta
def extract_text_from_multiple_pdfs(folder_path=pdf_folder):
    pdf_texts = {}
    if not os.path.exists(folder_path):
        print(f"❌ Pasta não encontrada: {folder_path}")
        return {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            pdf_texts[filename] = extract_text_from_pdf(pdf_path)
    return pdf_texts
