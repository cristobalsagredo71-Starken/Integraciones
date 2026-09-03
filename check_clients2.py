with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
matches = re.finditer(r'clients', js)
for m in matches:
    # Print the line where it occurs, but just the first few
    pass

lines = js.split('\n')
for i, line in enumerate(lines[:50]):
    if 'client' in line.lower():
        print(line)
