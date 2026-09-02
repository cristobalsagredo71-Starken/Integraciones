js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("section.className = 'panel';", "section.className = 'table-container';")
js = js.replace("table.className = 'table';", "table.className = 'data-grid';")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Fixed table styles")
