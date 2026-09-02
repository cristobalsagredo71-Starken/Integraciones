import re

html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Theme Toggle next to logo
theme_btn = '''
        <div style="display: flex; gap: 1rem; align-items: center;">
            <button id="theme-toggle" class="btn-icon tooltip-container">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                <span class="tooltip-text" style="bottom:-30px;">Cambiar Tema</span>
            </button>
'''
html = re.sub(r'(<div class="header">.*?)(</div>)', r'\1' + theme_btn + r'</div>\2', html, count=1, flags=re.DOTALL)

# 2. Add Bitacora section to Initiative Modal
bitacora_html = '''
            <div style="margin-top: 2rem; border-top: var(--border-width) solid var(--panel-border); padding-top: 1.5rem;">
                <h3 class="serif-title" style="margin-bottom: 1rem;">Bitácora de Proyecto</h3>
                
                <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                    <input type="text" id="input-log-text" class="form-control" placeholder="Añadir comentario o hito..." style="flex: 1;">
                    <button type="button" id="btn-add-log" class="btn btn-primary">Registrar</button>
                </div>
                
                <div id="logs-container" style="max-height: 200px; overflow-y: auto; background: var(--bg-color); padding: 1rem; border: var(--border-width) solid var(--panel-border); border-radius: var(--radius);">
                    <p style="color: var(--text-muted); font-size: 0.85rem; text-align: center;">No hay registros en la bitácora.</p>
                </div>
            </div>
'''
# Find the end of the form-row block for Initiative Modal and inject bitacora_html before the submit button
html = html.replace('<!-- Actions -->', bitacora_html + '\n            <!-- Actions -->')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated HTML")
