# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

# Create the FastAPI app
app = FastAPI(
    title="Mapa de Atributos API",
    description="Backend API for Mapa de Atributos",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mapa-de-atributos.vercel.app",
        "https://mapa-de-atributos-production.up.railway.app",
        # Add localhost for development
        "http://localhost:3000",
        "*"  # Consider removing this in production and being more specific
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include your router
app.include_router(router)

# Add a health check endpoint for Railway
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Run the application
if __name__ == "__main__":  # <-- Aqui estão faltando os underscores corretos
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
