import os
import json
import shutil
import urllib.parse

src_base = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\Starken2026\Proyectos\Integraciones"
dst_base = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\flows"

files_to_copy = [
    # Electrolux
    ("Integracion Electrolux\Discovery\discovery_electrolux_bultos.html", "Electrolux", "Discovery Bultos", "Electrolux (Vtex)"),
    ("Integracion Electrolux\Discovery\traspaso_informacion_electrolux_AS_IS.html", "Electrolux", "Traspaso Info AS-IS", "Electrolux (Vtex)"),
    ("Integracion Electrolux\Discovery\discovery_electrolux_outlets.html", "Electrolux", "Discovery Outlets", "Electrolux (Vtex)"),
    ("Integracion Electrolux\Discovery\Flujo AS-IS Integracion VTEX.html", "Electrolux", "Flujo AS-IS VTEX", "Electrolux (Vtex)"),
    ("Integracion Electrolux\Discovery\traspaso_informacion_electrolux.html", "Electrolux", "Traspaso Info", "Electrolux (Vtex)"),
    
    # Falabella
    ("Integracion Falabella\Discovery\Flujo_Integracion_Falabella.html", "Falabella", "Flujo Integración", "Falabella"),
    
    # Hites
    ("Integracion Hites\01_Resumen_Pedida_Hites.html", "Hites", "Resumen Pedida", "Hites"),
    
    # Ripley
    ("Integracion Ripley\Discovery\demo_ripley_hermanado.html", "Ripley", "Demo Hermanado", "Ripley"),
    ("Integracion Ripley\Discovery\propuesta_de_solucion_ripley.html", "Ripley", "Propuesta Solución", "Ripley"),
    
    # Walmart LI
    ("Integracion Walmart\Discovery\blueprint_logistica_inversa.html", "Walmart", "Blueprint LI", "Walmart LI"),
    ("Integracion Walmart\Discovery\comparativa_caminos_walmart.html", "Walmart", "Comparativa Caminos", "Walmart LI"),
    ("Integracion Walmart\Discovery\discovery_integracion_walmart.html", "Walmart", "Discovery Integración", "Walmart LI"),
    ("Integracion Walmart\Discovery\estrategia_encapsulamiento_infositio.html", "Walmart", "Estrategia Infositio", "Walmart LI"),
    ("Integracion Walmart\Discovery\flujo_diario_reagendamiento.html", "Walmart", "Flujo Reagendamiento", "Walmart LI"),
    ("Integracion Walmart\Discovery\flujo_saltarse_infositio.html", "Walmart", "Flujo Saltarse Infositio", "Walmart LI"),
]

flows_db = {}

for rel_path, folder_name, button_name, client_name in files_to_copy:
    src_path = os.path.join(src_base, rel_path)
    dst_folder = os.path.join(dst_base, folder_name)
    os.makedirs(dst_folder, exist_ok=True)
    
    file_name = os.path.basename(src_path)
    dst_path = os.path.join(dst_folder, file_name)
    
    # Copy file if source exists
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"Copied: {file_name}")
    else:
        print(f"Warning: Source not found -> {src_path}")
        
    # URL encoded for the web
    web_url = f"flows/{folder_name}/{urllib.parse.quote(file_name)}"
    
    if client_name not in flows_db:
        flows_db[client_name] = []
        
    flows_db[client_name].append({
        "name": button_name,
        "url": web_url
    })

# Add missing ones to keep JSON clean
for c in ["Shopify", "VTEX", "Walmart"]:
    if c not in flows_db:
        flows_db[c] = []

json_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\flows.json"
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(flows_db, f, indent=4, ensure_ascii=False)

print("Updated flows.json successfully!")
