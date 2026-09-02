with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

if "window.switchTab = (tabName) =>" in js:
    print("switchTab IS in JS.")
if "function renderCharts()" in js:
    print("renderCharts IS in JS.")
