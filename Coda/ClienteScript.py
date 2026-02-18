import pandas as pd
import requests

API_TOKEN = "9c9f5c1b-0443-4754-9ccc-0c65236a6117"
DOC_ID = "_neGgyqwZq"
TABLE_ID = "grid-gnGOIacgwg"

COLUMN_MAP = {
    "Expediente": "c-tDSasY_Fh3",
    "IP VPN": "c-1JKhripWs_",
    "ROUTER": "c-EXKmb6xQw5",
    "NAT": "c-vtNcC2ZXr4",
    "Empresa": "c-QiSZbyuoks",
    "Finca": "c-9OBYR-OoMN",
    "Pais": "c-Zpu1VcAwaT",
    "Provincia": "c-qs0xIwgTB9",
    "Municipio": "c-vJ0R_cG4qk",
    "Modelo Router": "c-V5Fgv8f7cQ",
    "Observaciones": "c-VSE3ZEvpLW"
}

df = pd.read_excel("ResumenClientesVPN.xlsx")

df = df.head(355)

rows = []

for _, row in df.iterrows():
    cells = []

    for excel_col, coda_col_id in COLUMN_MAP.items():
        if excel_col in df.columns and pd.notna(row[excel_col]):
            cells.append({
                "column": coda_col_id,
                "value": row[excel_col]
            })

    rows.append({"cells": cells})

url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}/rows"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json={"rows": rows})

print(response.status_code)
print(response.text)
