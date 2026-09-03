with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js_pmo = f.read()

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones-kam\app.js", "r", encoding="utf-8") as f:
    js_kam = f.read()

import re
match_pmo = re.search(r'const SUPABASE_URL = \'(.*?)\';\nconst SUPABASE_KEY = \'(.*?)\';', js_pmo)
match_kam = re.search(r'const SUPABASE_URL = \'(.*?)\';\nconst SUPABASE_KEY = \'(.*?)\';', js_kam)

if match_pmo and match_kam:
    print("PMO:", match_pmo.group(1), match_pmo.group(2)[:10] + "...")
    print("KAM:", match_kam.group(1), match_kam.group(2)[:10] + "...")
    if match_pmo.group(1) == match_kam.group(1) and match_pmo.group(2) == match_kam.group(2):
        print("MATCH! Same DB.")
    else:
        print("MISMATCH!")
else:
    print("Could not find connection strings")
