with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "return `" in line and "<tr>" in lines[i+1]:
        print("".join(lines[i:i+25]))
        break
