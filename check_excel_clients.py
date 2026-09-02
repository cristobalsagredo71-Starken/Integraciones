import pandas as pd
df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")
print("All Excel Clients:")
print(df['Client'].tolist()[:30])
