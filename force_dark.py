import re

# Update HTML
html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('<html lang="es">', '<html lang="es" data-theme="dark">')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Update JS
js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()
js = js.replace("localStorage.getItem('theme') || 'light'", "localStorage.getItem('theme') || 'dark'")
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Forced dark mode as default")
