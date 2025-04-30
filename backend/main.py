# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ⚠️ Use o do FastAPI!
from app.api import router

app = FastAPI(
    title="Mapa de Atributos API",
    description="Backend API for Mapa de Atributos",
    version="1.0.0"
)

# ✅ Definição correta dos domínios permitidos
origins = [
    "https://mapa-de-atributos.vercel.app",
    "http://localhost:3000"
]

# ✅ Middleware CORS corretamente configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ✅ Rotas incluídas
app.include_router(router)

# ✅ Endpoint de healthcheck
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# ✅ Execução local
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
