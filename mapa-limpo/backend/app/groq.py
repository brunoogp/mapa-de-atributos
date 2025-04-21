# app/groq.py
import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
import openai
from app.vectorstore.loader_arquetipos import load_vectorstore
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

# Cliente Groq direto
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

PROMPT_TEMPLATE = """
Você é um estrategista de marcas e deve gerar um diagnóstico em formato JSON **válido e parseável** com base no briefing e no conteúdo teórico a seguir. 

⚠️ IMPORTANTE:
- NÃO adicione nenhum comentário fora do JSON.
- NÃO explique o que está fazendo.
- NÃO use aspas desnecessárias, bullets ou pontuações extras.
- Use apenas os atributos fornecidos.
- Para os exemplos de marcas e arquétipos use apenas presentes nesse conteúdo de referência** as informações do banco vetorial.
- Retorne APENAS um JSON válido com a estrutura exata abaixo.

📚 Conteúdo de Referência (extraído do banco vetorial):
{pdf_contexto}

⚠️ Utilize **apenas os arquétipos presentes nesse conteúdo de referência**. Não adicione novos arquétipos, mesmo que pareçam fazer sentido. Respeite rigorosamente a lista e os detalhes dos PDFs.

📄 Briefing:
Nome da marca: {nome_marca}
Descrição: {descricao}
Atributos selecionados (use SOMENTE os atributos da lista abaixo): {atributos}
Demais informações relevantes:
{detalhes_extra}

📌 FORMATO EXATO DO JSON ESPERADO:
⚠️ Ao gerar a descrição do arquétipo e as diretrizes visual, verbal e simbólica, utilize apenas o conteúdo do banco vetorial correspondente ao arquétipo escolhido. NÃO invente, NÃO resuma de cabeça, NÃO use exemplos fora do que foi recuperado.

{{
  "resumo": "faça um resumo detalhado da empresa levando em consideração o contexto e os dados fornecidos na etapa 2 de briefing",
  "atributos": [{{"atributo": "Nome do Atributo", "valor": 0-10}}, ...],
  "arquetipo": {{
    "nome": "...",
    "descricao": "descreva sempre o arquétipo de forma objetiva e com bastnate detalhe, nunca fuja do contexto do arquétipo, se mantenha fiel as características dele de acordo com as informações do banco vetorial",
    "exemplos": ["...", "..."]
  }},
  "grafico_arquetipos": [{{"nome": "...", "valor": 0-100}}, ...],
 "diretrizes": {{
  "visual": "Com base nas referências visuais do arquétipo selecionado e considerando o contexto da empresa, descreva como a marca deve se manifestar visualmente. Inclua sugestões de estilo de identidade visual (formas, cores, tipografia), direção de arte, ambientações e sensações visuais que comuniquem o arquétipo de forma estratégica. Aponte também o que evitar visualmente para não descaracterizar a essência arquetípica.",
  "verbal": "Com base na linguagem e estilo comunicacional do arquétipo identificado, descreva como a marca deve se comunicar verbalmente com seu público. Indique o tom de voz ideal, estruturas de frases, vocabulário preferencial, além de exemplos práticos de como a marca pode se apresentar em textos institucionais, redes sociais ou campanhas. Adapte essas diretrizes à realidade da empresa e do setor.",
  "simbolico": "A partir do arquétipo dominante, recomende metáforas, narrativas simbólicas, ícones, elementos culturais e construções simbólicas que podem ser incorporadas na comunicação e identidade da marca. Traga sugestões de storytelling, personagens, analogias ou símbolos que fortaleçam o vínculo emocional com o público, de acordo com o contexto e posicionamento da marca."
}},

  "insights": [
  "Para cada atributo selecionado, gere um insight estratégico único e específico.",
  "A pontuação atribuída (0 a 10) indica a intensidade com que esse atributo precisa estar presente na comunicação para reforçar o arquétipo dominante.",
  "Evite frases genéricas e repetitivas como 'isso se conecta com...'. Use narrativas simbólicas, metáforas e tensão arquetípica.",
  "Inclua uma análise simbólica ou comportamental — como esse atributo contribui (ou não) para o impacto emocional da marca.",
  "Varie a linguagem de introdução e justificativa a cada insight. Explore construções como: 'Mais do que um atributo...', 'Funciona como um catalisador simbólico...', 'Traduz a intenção criativa da marca...', 'É um gesto de...'.",
  "Use metáforas visuais, sensoriais ou arquetípicas sempre que possível. Exemplo: 'Ser visionário é como abrir um novo caminho no nevoeiro da mesmice'.",
  "Sempre que pertinente, adicione uma tensão ou contraponto simbólico. Exemplo: 'Apesar de poderoso, esse atributo precisa ser dosado com clareza para não se tornar abstrato demais.'",
  "Sempre indique a pontuação atribuída (0 a 10) no final de cada insight, mesmo que o texto seja simbólico ou metafórico.",
  "Garanta que todos os atributos selecionados estejam presentes na resposta, sem omissões.",
  "Finalize a seção de insights com um parágrafo de síntese estratégica conectando os atributos ao arquétipo identificado, explicando como essa combinação reforça o posicionamento da marca.",
  "Exemplo de insight completo: 'Para um Criador, a agilidade não é apenas operacional — ela representa a liberdade criativa de testar, errar e evoluir rápido. Por isso, atribuímos 9/10 para esse atributo. Esse ritmo não só acelera processos, mas reforça a identidade de uma marca que não tem medo de transformar ideias em ação. Ainda assim, vale equilibrar esse impulso com consistência visual para manter clareza na entrega.'"
]


}}
"""

prompt_langchain = PromptTemplate(
    input_variables=["pdf_contexto", "nome_marca", "descricao", "atributos", "detalhes_extra"],
    template=PROMPT_TEMPLATE
)

def buscar_contexto_vetorial(contexto_briefing: dict):
    try:
        db = load_vectorstore()
        retriever = db.as_retriever(search_kwargs={"k": 8})
        query = f"{contexto_briefing['nome_marca']} - {contexto_briefing['descricao']}"
        llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))
        qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
        qa = RetrievalQA(retriever=retriever, combine_documents_chain=qa_chain, return_source_documents=True)
        resultado = qa.invoke({"query": query})
        docs_text = "\n\n".join([doc.page_content for doc in resultado["source_documents"]])
        print("✅ Contexto vetorial recuperado com sucesso")
        return docs_text
    except Exception as e:
        print(f"❌ Erro ao buscar contexto vetorial: {str(e)}")
        return "Erro ao carregar o contexto de referência."

def extrair_json(texto: str) -> dict:
    try:
        match = re.search(r"\{.*\}", texto, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        return json.loads(texto)
    except json.JSONDecodeError:
        texto_limpo = re.sub(r'^[^{]*', '', texto)
        texto_limpo = re.sub(r'[^}]*$', '', texto_limpo)
        try:
            return json.loads(texto_limpo)
        except json.JSONDecodeError as e:
            raise ValueError(f"❌ Não foi possível extrair um JSON válido. Erro: {str(e)}")

def iniciar_processamento(nome_marca, descricao, atributos, detalhes):
    try:
        print(f"🔍 Iniciando processamento para marca: {nome_marca}")
        detalhes_extra = "\n".join([f"{k}: {v}" for k, v in detalhes.items() if k not in ["nome_marca", "descricao_marca", "atributos_selecionados"]])
        contexto_briefing = {
            "query": f"{nome_marca} - {descricao}",
            "nome_marca": nome_marca,
            "descricao": descricao,
            "atributos": ", ".join(atributos),
            "detalhes_extra": detalhes_extra
        }

        print("🔍 Buscando contexto relevante na base de conhecimento...")
        pdf_contexto = buscar_contexto_vetorial(contexto_briefing)
        print(f"📄 Contexto vetorial:\n{pdf_contexto[:800]}...\n")

        print("🧠 Gerando diagnóstico estratégico com base no contexto encontrado...")
        resultado = gerar_diagnostico_com_llm(nome_marca, descricao, atributos, detalhes_extra, pdf_contexto)

        print("✅ Processamento completo")
        return resultado

    except Exception as e:
        print(f"❌ Erro no processamento: {str(e)}")
        raise e

import time

def gerar_diagnostico_com_llm(nome_marca, descricao, atributos, detalhes_extra, pdf_contexto):
    try:
        prompt_final = PROMPT_TEMPLATE.format(
            nome_marca=nome_marca,
            descricao=descricao,
            atributos=", ".join(atributos) if isinstance(atributos, list) else atributos,
            detalhes_extra=detalhes_extra,
            pdf_contexto=pdf_contexto
        )

        tentativas = 0
        while tentativas < 3:
            try:
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "system", "content": "Você é um estrategista de marcas especializado em arquétipos de marca."},
                        {"role": "user", "content": prompt_final},
                    ],
                    temperature=0.4,
                    max_tokens=4096,
                )

                content = response.choices[0].message.content
                print(f"✅ Resposta recebida do LLM")
                return extrair_json(content)

            except openai.RateLimitError as e:
                print("⚠️ Limite de tokens atingido. Aguardando 65 segundos para tentar novamente...")
                time.sleep(65)
                tentativas += 1

        raise RuntimeError("❌ Limite de requisições excedido após várias tentativas.")

    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Erro ao gerar diagnóstico: {str(e)}")
        raise


        content = response.choices[0].message.content
        print(f"✅ Resposta recebida do LLM")
        return extrair_json(content)

    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {str(e)}")
        raise
    except Exception as e:
        print(f"❌ Erro ao gerar diagnóstico: {str(e)}")
        raise

def gerar_diagnostico_com_groq(nome_marca, descricao, atributos, detalhes, pdf_texts=None):
    print("⚠️ Usando função legada. Considere usar iniciar_processamento() diretamente.")
    return iniciar_processamento(nome_marca, descricao, atributos, detalhes)
