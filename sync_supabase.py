import pandas as pd
import urllib.request
import json

# 1. Load Excel Data
df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")

# Mapping Maestro Name -> Excel Name
MAPPING = {
    "Walmart LI": "GRUPO WALMART",
    "Ripley": "GRUPO RIPLEY",
    "Falabella": "FALATALE CHILE SPA",
    "Cencosud": "GRUPO CENCOSUD",
    "Easy": "ADORA DE PROCESOS S.A. CENCOSU",
    "Decatlhon": "CHILE SPA  DECATHLON",
    "Electrolux": "GRUPO ELECTROLUX",
    "Hites ": "GRUPO HITES",
    "Arrimaq": "ARRIMAQ"
}

SUPABASE_URL = "https://dzmsfxnvfardckddvzjt.supabase.co/rest/v1/clients"
SUPABASE_KEY = "sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

# 2. Fetch current clients
req = urllib.request.Request(SUPABASE_URL + "?select=*", headers=HEADERS)
with urllib.request.urlopen(req) as response:
    clients = json.loads(response.read().decode())

print(f"Loaded {len(clients)} clients from Supabase.")

for client in clients:
    db_name = client["name"]
    if db_name in MAPPING:
        excel_name = MAPPING[db_name]
        
        # Find row in Excel
        row = df[df['Client'] == excel_name]
        if row.empty:
            print(f"WARNING: Could not find {excel_name} in Excel.")
            continue
            
        row = row.iloc[0]
        
        # Extract Promedio Mensual
        promedio = row.get("Promedio Mensual", 0)
        if pd.isna(promedio): promedio = 0
        
        # Extract Monthly History (Columns 1 to 7)
        # Months in Supabase are expected like "2026-07"
        history = []
        for month_num in range(1, 8):
            if month_num in row.index:
                val = row[month_num]
                if pd.isna(val): val = 0
                month_str = f"2026-{month_num:02d}"
                history.append({
                    "month": month_str,
                    "volume": 0, # Assuming volume isn't provided in this Excel
                    "revenue": int(val)
                })
        
        # We need to sort descending because the frontend expects it latest first
        history.sort(key=lambda x: x["month"], reverse=True)
        
        # 3. Patch Supabase
        update_data = {
            "revenue": int(promedio),
            "monthly_history": history
        }
        
        patch_req = urllib.request.Request(
            SUPABASE_URL + f"?id=eq.{client['id']}", 
            data=json.dumps(update_data).encode("utf-8"), 
            headers=HEADERS, 
            method="PATCH"
        )
        
        try:
            with urllib.request.urlopen(patch_req) as p_response:
                print(f"SUCCESS: Updated {db_name} (revenue: {int(promedio)})")
        except Exception as e:
            print(f"FAILED: Could not update {db_name}: {e}")
    else:
        print(f"SKIPPED: {db_name} not in mapping.")

print("Sync complete.")
