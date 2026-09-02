import json
json_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\flows.json"
with open(json_path, 'r', encoding='utf-8-sig') as f:
    flows_db = json.load(f)
if "Conductor Regular" not in flows_db:
    flows_db["Conductor Regular"] = []
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(flows_db, f, indent=4, ensure_ascii=False)
print("Added Conductor Regular to flows.json")
