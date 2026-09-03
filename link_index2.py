with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
target = '<button type="button" class="btn-icon tooltip-container" onclick="toggleTheme()">'
replacement = '<a href="kam.html" class="badge-tag" style="background: rgba(29, 78, 216, 0.1); color: var(--text-main); text-decoration: none; margin-right: 15px; border: 1px solid var(--panel-border); font-size: 0.8rem; padding: 6px 12px; border-radius: 20px;">Ir a Vista KAM →</a>\n          <button type="button" class="btn-icon tooltip-container" onclick="toggleTheme()">'

html = html.replace(target, replacement)
with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Link added successfully")
