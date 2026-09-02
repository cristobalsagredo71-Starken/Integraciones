import pandas as pd
df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")
clients = df['Client'].dropna().tolist()
matches = [(c, df[df['Client'] == c].iloc[0]['Total 2026'], df[df['Client'] == c].iloc[0]['Promedio Mensual']) for c in clients if "ELECTROLUX" in c.upper()]
print("Matches for ELECTROLUX:", matches)
