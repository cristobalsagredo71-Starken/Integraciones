with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
matches = re.finditer(r'(?:let|const|var)\s+clients\b', js)
for m in matches:
    print(js[max(0, m.start()-50):m.end()+50])
