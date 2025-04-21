# backend/app/sheets.py

import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1--YM0Av6A2cHa5NU8JfYbFn1I0VHov5mRbQhIzKEsvE"  # substitua pelo seu se mudar
SHEET_NAME = "Página1"  # nome da aba
SERVICE_ACCOUNT_FILE = "credentials.json"

def adicionar_linha(dados: list):
    print("DEBUG - Dados recebidos:", dados)

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
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
