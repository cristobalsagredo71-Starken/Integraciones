import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Find the button we just added
old_btn = r"""\$\{\(init\.logs && init\.logs\.length > 0\) \? `<button type="button" onclick="event\.stopPropagation\(\); toggleBitacora\('\$\{init\.id\}'\)" class="badge-tag tooltip-container" style="background: transparent; border: 1px solid var\(--text-muted\); cursor: pointer; margin-left: 8px;">📖 <span class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX\(-50%\); width: max-content;">Ver Bitácora \(\$\{init\.logs\.length\}\)</span></button>` : ''\}"""

# Replace it with the Jira/Confluence styled button
new_btn = r"""${(init.logs && init.logs.length > 0) ? `<button type="button" onclick="event.stopPropagation(); toggleBitacora('${init.id}')" class="badge-tag" style="background: rgba(107, 114, 128, 0.2); color: var(--text-muted); border: 1px solid rgba(107, 114, 128, 0.4); text-decoration: none; margin-top: 4px; display: inline-block; margin-left: 4px; cursor: pointer;">Bitácora (${init.logs.length}) 📖</button>` : ''}"""

js = re.sub(old_btn, new_btn, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS for button style")
