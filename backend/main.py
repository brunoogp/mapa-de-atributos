from fastapi import FastAPI
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mapa-de-atributos.vercel.app"],  # 👈 Aqui!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
