import os
from fastapi import APIRouter
from pydantic import BaseModel, validator
from typing import List
from app.sheets import adicionar_linha
from app.groq import gerar_diagnostico_com_groq
from app.pdf_extractor import extract_text_from_multiple_pdfs

router = APIRouter()

# Caminho para a pasta onde estão os PDFs
pdf_folder = os.path.join(os.path.dirname(__file__), "pdf_contexto")

class Briefing(BaseModel):
    nome_marca: str
    descricao_marca: str
    atributos_selecionados: List[str]
    nome: str
    email: str
    site: str
    localizacao: str
    segmento: str
    tempoExistencia: str
    temIdentidade: bool
    canais: str
    mensagemMarca: str
    valores: str
    percepcao: str
    publicoIdeal: str
    transformacao: str
    concorrentes: str
    diferencial: str
    objetivo: str
    receberResumo: bool

    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Email inválido")
        return v

@router.post("/diagnostico/briefing-direto")
def diagnostico_direto(briefing: Briefing):
    # Organiza os dados em ordem desejada para a planilha
    dados_para_planilha = [
        briefing.nome,
        briefing.email,
        briefing.nome_marca,
        briefing.site,
        briefing.localizacao,
        briefing.segmento,
        briefing.tempoExistencia,
        "Sim" if briefing.temIdentidade else "Não",
        briefing.canais,
        briefing.descricao_marca,
        briefing.mensagemMarca,
        briefing.valores,
        briefing.percepcao,
        briefing.publicoIdeal,
        briefing.transformacao,
        briefing.concorrentes,
        briefing.diferencial,
        briefing.objetivo,
        ", ".join(briefing.atributos_selecionados),
        "Sim" if briefing.receberResumo else "Não"
    ]

    # Adiciona na planilha
    adicionar_linha(dados_para_planilha)

    # Extrai contexto dos PDFs
    pdf_texts = extract_text_from_multiple_pdfs(pdf_folder)
    print("🗂️ PDFs lidos:", list(pdf_texts.keys()))

    # Geração com base no briefing + PDFs
    resultado = gerar_diagnostico_com_groq(
        nome_marca=briefing.nome_marca,
        descricao=briefing.descricao_marca,
        atributos=briefing.atributos_selecionados,
        detalhes=briefing.dict(),  # <- CORRETO
        pdf_texts=pdf_texts
    )

    return resultado
