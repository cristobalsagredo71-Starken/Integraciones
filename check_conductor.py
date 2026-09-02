with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()
import re
match = re.search(r'<div[^>]*id="view-conductor"[^>]*>', html)
if match:
    print(match.group(0))
else:
    print("view-conductor NOT FOUND either!")
