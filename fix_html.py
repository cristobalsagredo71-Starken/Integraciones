html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace("switchTab(\\'sistemas\\')", "switchTab('sistemas')")
html = html.replace("switchTab(\\'conductor\\')", "switchTab('conductor')")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed HTML backslashes")
