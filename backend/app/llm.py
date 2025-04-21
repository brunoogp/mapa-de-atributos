# backend/app/llm.py
def gerar_diagnostico(briefing: str, atributos: list[str]) -> dict:
    # Aqui futuramente vamos usar LangChain + Chroma + Groq
    return {
        "arquetipo": "O Cuidador",
        "descricao": "Focado em proteger, cuidar e gerar bem-estar...",
        "insights": [
            "Alta coerência entre os atributos e o arquétipo.",
            "Potencial de diferenciação com foco em cuidado."
        ],
        "graficos": {
            "atributos": [{"atributo": a, "valor": 7 + i % 3} for i, a in enumerate(atributos)],
            "arquétipos": [
                {"nome": "O Cuidador", "valor": 92},
                {"nome": "O Inocente", "valor": 85},
                {"nome": "O Sábio", "valor": 68}
            ]
        }
    }
