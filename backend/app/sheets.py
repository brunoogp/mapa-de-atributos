# backend/app/sheets.py

import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1--YM0Av6A2cHa5NU8JfYbFn1I0VHov5mRbQhIzKEsvE"  # substitua se mudar
SHEET_NAME = "Página1"  # nome da aba

# Carrega o JSON de credenciais da variável de ambiente
SERVICE_ACCOUNT_INFO = json.loads(os.environ["GOOGLE_CREDENTIALS"])

def adicionar_linha(dados: list):
    print("DEBUG - Dados recebidos:", dados)

    creds = Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    # Cada item da lista vira uma célula em uma linha
    valores = [dados]

    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="USER_ENTERED",
        body={"values": valores}
    ).execute()
