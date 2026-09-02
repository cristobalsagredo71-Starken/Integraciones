import pandas as pd
df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")
clients = df['Client'].dropna().tolist()
matches = [c for c in clients if "FALA" in c.upper()]
print("Matches for FALA:", matches)
