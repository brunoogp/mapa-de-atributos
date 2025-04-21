from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Briefing(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    nome_marca: str
    descricao_marca: str
    mercado_atuacao: str
    concorrentes: Optional[str] = None
    objetivo: Optional[str] = None
    valores_principais: Optional[str] = None
    tom_voz: Optional[str] = None
    palavras_chave: Optional[List[str]] = []
    atributos_selecionados: Optional[List[str]] = []
