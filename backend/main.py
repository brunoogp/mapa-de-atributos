# main.py
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api import router

app = FastAPI(
    title="Mapa de Atributos API",
    description="Backend API for Mapa de Atributos",
    version="1.0.0"
)

# ✅ CORRETAMENTE CONFIGURADO
origins = [
    "https://mapa-de-atributos.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Suas rotas
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
