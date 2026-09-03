with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

idx = js.find("'submit'")
if idx != -1:
    print(js[max(0, idx-100):min(len(js), idx+500)])
else:
    print("Submit not found")
