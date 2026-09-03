import os
import shutil

pmo_dir = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones"
kam_dir = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones-kam"

if not os.path.exists(kam_dir):
    os.makedirs(kam_dir)

# Move and rename kam.html -> index.html
if os.path.exists(os.path.join(pmo_dir, "kam.html")):
    shutil.move(os.path.join(pmo_dir, "kam.html"), os.path.join(kam_dir, "index.html"))

# Move and rename kam.js -> app.js
if os.path.exists(os.path.join(pmo_dir, "kam.js")):
    shutil.move(os.path.join(pmo_dir, "kam.js"), os.path.join(kam_dir, "app.js"))

# Copy styles.css
shutil.copy2(os.path.join(pmo_dir, "styles.css"), os.path.join(kam_dir, "styles.css"))

# Revert the PMO index.html to remove the KAM link
with open(os.path.join(pmo_dir, "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'<a href="kam.html"[^>]*>Ir a Vista KAM →</a>\n\s*', '', html)
with open(os.path.join(pmo_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

# Clean up KAM index.html to point to app.js instead of kam.js, and remove "Volver a PMO"
with open(os.path.join(kam_dir, "index.html"), "r", encoding="utf-8") as f:
    k_html = f.read()

k_html = k_html.replace('src="kam.js"', 'src="app.js"')
k_html = re.sub(r'<a href="index.html"[^>]*>← Volver a PMO</a>\n\s*', '', k_html)
with open(os.path.join(kam_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(k_html)

print("Split completed")
