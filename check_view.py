with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
match = re.search(r'view-metricas', html)
if match:
    print("view-metricas found!")
else:
    print("NOT FOUND")
