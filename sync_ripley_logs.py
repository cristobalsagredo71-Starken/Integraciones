import json
import urllib.request

SUPABASE_URL = "https://dzmsfxnvfardckddvzjt.supabase.co/rest/v1/initiatives"
SUPABASE_KEY = "sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

LOGS_MAP = {
    "Ripley - ": [
        {"date": "2026-08-30 12:00", "author": "Bitácora Importada", "text": "REUNIÓN: Seguimiento modelo In-House Ripley e integración Ripley. Revisión de continuidad y próximos pasos. 【3-bcdee3】"},
        {"date": "2026-08-20 12:00", "author": "Bitácora Importada", "text": "ESTADO TÉCNICO: Se genera ticket PRY-44 para evaluación, cubicación y priorización técnica."},
        {"date": "2026-06-25 12:00", "author": "Bitácora Importada", "text": "HITO: Discovery Proyecto Integraciones Ripley finalizado. Se levantan requerimientos y alcance inicial. 【2-89ad31】"},
        {"date": "2026-06-15 12:00", "author": "Bitácora Importada", "text": "INICIO: Primer acercamiento formal Ripley / Starken para revisar oportunidad de integración. 【1-58564f】"}
    ]
}

req = urllib.request.Request(SUPABASE_URL + "?select=id,name", headers=HEADERS)
with urllib.request.urlopen(req) as response:
    inits = json.loads(response.read().decode())

for i in inits:
    name = i['name']
    match_key = next((k for k in LOGS_MAP if k in name), None)
    if match_key:
        logs = LOGS_MAP[match_key]
        patch_req = urllib.request.Request(
            SUPABASE_URL + f"?id=eq.{i['id']}", 
            data=json.dumps({"logs": logs}).encode("utf-8"), 
            headers=HEADERS, 
            method="PATCH"
        )
        try:
            with urllib.request.urlopen(patch_req):
                print(f"Updated logs for {name}")
        except Exception as e:
            print(f"Failed to update {name}: {e}")
