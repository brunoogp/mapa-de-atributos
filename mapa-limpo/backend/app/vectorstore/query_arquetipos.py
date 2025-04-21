from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os
from dotenv import load_dotenv

# 🔐 Carrega as variáveis de ambiente (.env com sua chave da OpenAI)
load_dotenv()

# 🔁 Carrega a base vetorial existente
persist_directory = "app/vectorstore/index"

# Inicializa embeddings e base Chroma
embedding = OpenAIEmbeddings()
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

# Inicializa modelo de linguagem
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Cria a chain de QA com recuperação por similaridade
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

# 📥 Sua pergunta aqui
pergunta = "Qual arquétipo representa uma marca inovadora e rebelde?"

# 🔍 Realiza a consulta
resposta = qa_chain(pergunta)

# ✅ Exibe a resposta
print("\n🔎 Pergunta:", pergunta)
print("\n💬 Resposta:", resposta['result'])

# 📝 Fontes
print("\n📚 Fontes:")
for doc in resposta["source_documents"]:
    print("-", doc.metadata.get("source", ""))
