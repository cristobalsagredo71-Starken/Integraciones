with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "view-metricas" in line:
        start = max(0, i-5)
        end = min(len(lines), i+15)
        print("".join(lines[start:end]))
        break
