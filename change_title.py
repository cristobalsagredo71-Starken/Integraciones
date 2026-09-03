with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'<h1 style="[^"]*">Maestro Integraciones</h1>', r'<h1 style="font-family: \'Playfair Display\', serif; font-size: 1.8rem; margin: 0; display: flex; align-items: center; color: var(--text-main);">Maestro Integraciones Proyectos</h1>', html)
# just in case it's not strictly that string:
html = html.replace(">Maestro Integraciones</h1>", ">Maestro Integraciones Proyectos</h1>")
html = html.replace("<title>Starken | Maestro de Integraciones</title>", "<title>Starken | Maestro Integraciones Proyectos</title>")

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Title changed")
