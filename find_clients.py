import pandas as pd
df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")
clients = df['Client'].tolist()
for search_term in ["FALA", "RIP", "HITES", "DECA", "EASY", "ARRENDAMIENTO"]:
    matches = [c for c in clients if isinstance(c, str) and search_term in c.upper()]
    print(f"Matches for {search_term}: {matches}")
