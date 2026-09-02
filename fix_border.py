js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("var(--border-color)", "var(--panel-border)")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Fixed border color variable")
