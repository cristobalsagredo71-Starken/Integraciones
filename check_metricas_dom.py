with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "view-metricas" in line:
        start = max(0, i-25)
        end = min(len(lines), i+5)
        print("".join(lines[start:end]))
        break
