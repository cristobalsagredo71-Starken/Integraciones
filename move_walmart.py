import json

json_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\flows.json"
with open(json_path, 'r', encoding='utf-8-sig') as f:
    flows_db = json.load(f)

homologacion = flows_db.pop("Walmart - Homologación de estados.", [])
reagendamientos = flows_db.get("Walmart LI - Reagendamientos", [])

reagendamientos.extend(homologacion)
flows_db["Walmart LI - Reagendamientos"] = reagendamientos

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(flows_db, f, indent=4, ensure_ascii=False)

print("Moved Walmart flows to Reagendamientos")
