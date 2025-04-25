from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mapa-de-atributos.vercel.app"],  # 🔥 use somente o domínio da Vercel
    allow_credentials=True,
    allow_methods=["*"],  # ou ["POST"] se quiser restringir
    allow_headers=["*"]
)

app.include_router(router)
