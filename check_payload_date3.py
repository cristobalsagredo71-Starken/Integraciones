with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

idx = js.find('const payload = {', js.find('const payload = {') + 10)
print(js[idx+600:idx+1200])
