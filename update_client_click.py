import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

target = r'const tr = document\.createElement\(\'tr\'\);\s*tr\.innerHTML = `'

replacement = r'''const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.className = 'client-row';
        tr.onclick = (e) => {
            if (!e.target.closest('button') && !e.target.closest('a')) {
                editClient(clientData.id);
            }
        };
        tr.innerHTML = `'''

js = re.sub(target, replacement, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated renderClientsGrid")
