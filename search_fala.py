import pandas as pd
df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")
clients = df['Client'].dropna().tolist()

search_terms = ["FALA", "SACI", "SODIMAC", "TOTTUS", "LINIO", "IKEA", "FAZIL", "RETAIL"]
for term in search_terms:
    matches = [c for c in clients if term in c.upper()]
    if matches:
        print(f"Matches for {term}: {matches}")

print("\n--- TOP 30 CLIENTS ---")
print(clients[:30])
