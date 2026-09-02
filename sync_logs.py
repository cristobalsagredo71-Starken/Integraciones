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
    "Walmart -": [
        {"date": "2026-09-01 12:00", "author": "Bitácora Importada", "text": "ALERTA COMERCIAL: Cliente presiona por ETA de despliegue. Dependencia crítica de TI para iniciar desarrollo."},
        {"date": "2026-08-25 12:00", "author": "Bitácora Importada", "text": "DEFINICIÓN CERRADA: Walmart aprueba y entrega homologación final de estados."},
        {"date": "2026-08-11 12:00", "author": "Bitácora Importada", "text": "REUNIÓN: Reunión formal para propuesta de homologación STK-Walmart."}
    ],
    "Ripley -": [
        {"date": "2026-08-30 12:00", "author": "Bitácora Importada", "text": "REUNIÓN: Seguimiento modelo In-House Ripley."},
        {"date": "2026-08-20 12:00", "author": "Bitácora Importada", "text": "ESTADO TÉCNICO: Se genera ticket formal (PRY-44) para evaluación y priorización técnica en backlog."},
        {"date": "2026-06-25 12:00", "author": "Bitácora Importada", "text": "HITO: Discovery cerrado."}
    ],
    "Homologacion de estado Retail": [
        {"date": "2026-08-18 12:00", "author": "Bitácora Importada", "text": "REQUERIMIENTO CUSTOM: Cliente exige adaptación específica del flujo de estados. Se define que es un desarrollo exclusivo (no correctivo transversal)."},
        {"date": "2026-07-06 12:00", "author": "Bitácora Importada", "text": "HITO: Revisión inicial del modelo de integración."}
    ],
    "Decatlhon": [
        {"date": "2026-08-18 14:00", "author": "Bitácora Importada", "text": "INCIDENCIA: Gestión de errores 401 desde la API del cliente en producción."},
        {"date": "2026-08-18 12:00", "author": "Bitácora Importada", "text": "GO LIVE: Despliegue productivo reportado (Kick-off Trackbox)."},
        {"date": "2026-07-21 12:00", "author": "Bitácora Importada", "text": "HITO: Reunión inicial de integración."}
    ],
    "Electrolux -": [
        {"date": "2026-07-22 12:00", "author": "Bitácora Importada", "text": "EVALUACIÓN: Análisis comercial y de facturación enviado. A la espera de viabilidad técnica/negocio para avanzar a Discovery."}
    ],
    "Hites": [
        {"date": "2026-08-05 12:00", "author": "Bitácora Importada", "text": "HITO: Reunión inicial de acercamiento. (Sin avance posterior registrado)."}
    ]
}

# Fetch
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

print("Sync complete.")
