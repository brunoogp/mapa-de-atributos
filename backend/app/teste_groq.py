from groq import gerar_diagnostico_com_groq

nome_marca = "Lumenia"
descricao = "A Lumenia é uma marca de tecnologia sustentável que desenvolve produtos eletrônicos com design minimalista e materiais recicláveis. Nosso propósito é iluminar um futuro mais consciente e inovador."

atributos = [
    "inovadora", "sustentável", "minimalista", "tecnológica", "autêntica",
    "visionária", "responsável", "eficiente", "amigável", "confiável"
]

detalhes = {
    "publico_alvo": "Profissionais criativos e conscientes ambientalmente, entre 25 e 40 anos.",
    "diferenciais": "Design exclusivo, uso de materiais recicláveis, tecnologia de ponta com baixo consumo energético.",
    "valores": "Inovação, transparência, responsabilidade ambiental.",
    "visao": "Ser referência global em tecnologia com propósito."
}

resposta = gerar_diagnostico_com_groq(nome_marca, descricao, atributos, detalhes)

import json
print(json.dumps(resposta, indent=2, ensure_ascii=False))
