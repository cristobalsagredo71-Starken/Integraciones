import os
import json
import shutil
import urllib.parse

src_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\Starken2026\Proyectos\Integraciones\Integracion Ripley\Discovery\exposicion_casos_inhouse.html"
dst_folder = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\flows\Ripley"
json_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\flows.json"

os.makedirs(dst_folder, exist_ok=True)
file_name = os.path.basename(src_path)
dst_path = os.path.join(dst_folder, file_name)

if os.path.exists(src_path):
    shutil.copy2(src_path, dst_path)
    print(f"Copied: {file_name}")
else:
    print(f"Error: {src_path} not found")

with open(json_path, 'r', encoding='utf-8') as f:
    flows_db = json.load(f)

web_url = f"flows/Ripley/{urllib.parse.quote(file_name)}"
button_name = "Exposición Casos InHouse"

# Check if already exists to avoid duplicates
exists = any(item['url'] == web_url for item in flows_db.get("Ripley", []))
if not exists:
    if "Ripley" not in flows_db:
        flows_db["Ripley"] = []
    flows_db["Ripley"].append({
        "name": button_name,
        "url": web_url
    })
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(flows_db, f, indent=4, ensure_ascii=False)
    print("Updated flows.json successfully!")
else:
    print("Already in flows.json")
