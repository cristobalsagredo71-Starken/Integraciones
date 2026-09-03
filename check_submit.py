with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
match = re.search(r"document\.getElementById\('form-init'\)\.addEventListener\('submit', async \(e\) => \{.*?\n\}\);", js, re.DOTALL)
if match:
    print(match.group(0)[:1000])
else:
    print("Could not find form-init event listener")
