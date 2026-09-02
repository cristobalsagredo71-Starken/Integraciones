import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add window.toggleBitacora
if "window.toggleBitacora" not in js:
    toggle_func = """\nwindow.toggleBitacora = (id) => {
    const el = document.getElementById('bitacora-' + id);
    if (el) {
        el.style.display = el.style.display === 'none' ? 'table-row' : 'none';
    }
};\n"""
    js = js.replace("const renderInitRow =", toggle_func + "const renderInitRow =")

# 2. Add the button to the Initiative Name column
name_target = """<strong style="font-size: 1.05rem;">${init.name}</strong> ${getFlowsHtml(init.name)}"""
name_replacement = """<strong style="font-size: 1.05rem;">${init.name}</strong> ${getFlowsHtml(init.name)}
                    ${(init.logs && init.logs.length > 0) ? `<button type="button" onclick="event.stopPropagation(); toggleBitacora('${init.id}')" class="badge-tag tooltip-container" style="background: transparent; border: 1px solid var(--text-muted); cursor: pointer; margin-left: 8px;">📖 <span class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content;">Ver Bitácora (${init.logs.length})</span></button>` : ''}"""
js = js.replace(name_target, name_replacement)

# 3. Modify the nested TR to have an ID and display: none
row_target = """<tr style="background: var(--bg-color);">"""
row_replacement = """<tr id="bitacora-${init.id}" style="display: none; background: var(--bg-color);">"""
js = js.replace(row_target, row_replacement)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS for toggleable bitacora")
