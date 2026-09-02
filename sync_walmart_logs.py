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
    "Walmart LI - Reagendamientos": [
        {"date": "2026-08-20 12:00", "author": "Bitácora Importada", "text": "ESTADO TÉCNICO: Pendiente OK definitivo para iniciar desarrollo con el proveedor (Cotización MR1578)."},
        {"date": "2026-08-17 12:00", "author": "Bitácora Importada", "text": "DEFINICIÓN CERRADA: Creación de tarjeta PRY-58 documentando reglas de negocio, SLA y validaciones."},
        {"date": "2026-08-11 12:00", "author": "Bitácora Importada", "text": "HITO: Infositio entrega cotización MR1578."},
        {"date": "2026-08-05 12:00", "author": "Bitácora Importada", "text": "ALERTA COMERCIAL: Walmart en espera de cotización Starken."},
        {"date": "2026-07-31 12:00", "author": "Bitácora Importada", "text": "REUNIÓN: Mesa Walmart + DispatchTrack + Starken para revisar flujo."},
        {"date": "2026-07-09 12:00", "author": "Bitácora Importada", "text": "DEFINICIÓN CERRADA: Acuerdo funcional. Reagendamiento usará mismo webhook, cancelará retiro anterior y creará uno nuevo."}
    ],
    "Walmart - Homologaci": [
        {"date": "2026-09-01 12:00", "author": "Bitácora Importada", "text": "ALERTA COMERCIAL: Formalización en PRY-70. Walmart presiona por ETA e implementación para nuevos sellers."},
        {"date": "2026-08-25 12:00", "author": "Bitácora Importada", "text": "DEFINICIÓN CERRADA: Walmart devuelve homologación finalizada."},
        {"date": "2026-08-11 12:00", "author": "Bitácora Importada", "text": "REUNIÓN: Sesión formal de homologación y entrega de catálogo de estados a Walmart."},
        {"date": "2026-08-07 12:00", "author": "Bitácora Importada", "text": "HITO: Intervención Comercial/TI para resolver dudas operativas (CATEX, siniestros, devoluciones)."},
        {"date": "2026-07-31 12:00", "author": "Bitácora Importada", "text": "ESTADO TÉCNICO: Inicio formal. Se solicita revisión de descuadres de estados entre Starken y Dispatch."}
    ]
}

# Fetch all initiatives to find exact IDs
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
