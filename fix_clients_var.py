with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("[...clients].filter", "[...clientsData].filter")

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "w", encoding="utf-8") as f:
    f.write(js)
print("Replaced clients with clientsData")
