import pandas as pd
import urllib.request
import json

df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")

MAPPING = {
    "Electrolux": "GRUPO ELECTROLUX"
}

SUPABASE_URL = "https://dzmsfxnvfardckddvzjt.supabase.co/rest/v1/clients"
SUPABASE_KEY = "sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

req = urllib.request.Request(SUPABASE_URL + "?select=*", headers=HEADERS)
with urllib.request.urlopen(req) as response:
    clients = json.loads(response.read().decode())

for client in clients:
    db_name = client["name"]
    if db_name in MAPPING:
        excel_name = MAPPING[db_name]
        
        row = df[df['Client'] == excel_name]
        if row.empty:
            continue
            
        row = row.iloc[0]
        
        promedio = row.get("Promedio Mensual", 0)
        if pd.isna(promedio): promedio = 0
        
        history = []
        for month_num in range(1, 8):
            if month_num in row.index:
                val = row[month_num]
                if pd.isna(val): val = 0
                history.append({
                    "month": f"2026-{month_num:02d}",
                    "volume": 0,
                    "revenue": int(val)
                })
        
        history.sort(key=lambda x: x["month"], reverse=True)
        
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

print("Correction complete.")
