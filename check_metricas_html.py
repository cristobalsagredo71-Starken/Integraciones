import re
with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

if "chart.js" in html:
    print("Chart.js script IS in HTML.")
else:
    print("Chart.js script is MISSING in HTML.")

if "id=\"view-metricas\"" in html:
    print("view-metricas IS in HTML.")
else:
    print("view-metricas is MISSING in HTML.")
