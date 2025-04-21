import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_vectorstore():
    persist_directory = os.path.join(os.path.dirname(__file__), "arquetipos")
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    return vectordb

if __name__ == "__main__":
    print("📥 Iniciando ingestão de arquétipos...")

    file_path = os.path.join(os.path.dirname(__file__), "todos_os_arquetipos.md")
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    persist_directory = os.path.join(os.path.dirname(__file__), "arquetipos")
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embedding,
        persist_directory=persist_directory
    )

    vectordb.persist()
    print("✅ Base vetorial salva com sucesso em:", persist_directory)
