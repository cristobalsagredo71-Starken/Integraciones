with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

idx = html.find('input-estimated-date')
print(html[idx-1000:idx+100])
