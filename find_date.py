with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
matches = re.finditer(r'<input type="date".*?>', html)
for m in matches:
    print(m.group(0))
