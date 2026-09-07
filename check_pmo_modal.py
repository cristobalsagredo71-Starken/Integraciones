with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
matches = re.finditer(r'modal.*?(active|flex|block|display|show|style).*?\n', js)
for m in matches:
    print(m.group(0))
