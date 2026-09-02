with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
match = re.search(r'window\.switchTab = .*?\}', js, re.DOTALL)
print(match.group(0))
