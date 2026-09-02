import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

target = r'<tr>\s*<td><strong>\$\{c\.name\}</strong>'
replacement = r'''<tr style="cursor:pointer;" class="client-row" onclick="if(!event.target.closest('button') && !event.target.closest('a')) editClient('${c.id}');">
                        <td><strong>${c.name}</strong>'''
js = re.sub(target, replacement, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated renderSistemasGrid clicks")
