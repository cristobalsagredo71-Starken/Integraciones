with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
header_target = '<div class="header-right">'
header_replacement = '<div class="header-right">\n          <a href="kam.html" class="badge-tag" style="background: rgba(29, 78, 216, 0.1); color: var(--text-main); text-decoration: none; margin-right: 15px; border: 1px solid var(--panel-border);">Ir a Vista KAM →</a>'

if header_target in html and "Ir a Vista KAM" not in html:
    html = html.replace(header_target, header_replacement)
    with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Added link to index.html")
else:
    print("Link already exists or target not found")
