try:
    import pandas as pd
    import openpyxl
    df = pd.read_excel(r"C:\Users\cristobal.sagredo\Downloads\Reporte_General_Aportes_2026.xlsx")
    print(df.head())
    print("Columns:", df.columns.tolist())
except Exception as e:
    print("Error:", e)
