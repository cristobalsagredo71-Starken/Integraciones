import os
import re

html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
kam_html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\kam.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace scripts
html = html.replace('src="app.js"', 'src="kam.js"')
# Replace title
html = html.replace('>Maestro Integraciones Proyectos</h1>', '>Maestro Integraciones KAM</h1>')
html = html.replace('<title>Starken | Maestro Integraciones Proyectos</title>', '<title>Starken | Maestro KAM</title>')

# Inject switch link in header
header_target = '<div class="header-right">'
header_replacement = '<div class="header-right">\n          <a href="index.html" class="badge-tag" style="background: rgba(107, 114, 128, 0.2); color: var(--text-muted); text-decoration: none; margin-right: 15px; border: 1px solid var(--panel-border);">← Volver a PMO</a>'
html = html.replace(header_target, header_replacement)

# Remove the metricas div and conductor view entirely
html = re.sub(r'<!-- VISTA CONDUCTOR REGULAR -->.*?(?=<div id="modal-client")', '', html, flags=re.DOTALL)
# Remove toolbar totally
html = re.sub(r'<div class="toolbar">.*?</div>\s*</div>', """
      <div class="toolbar" style="display: flex; gap: 1rem; align-items: center; padding: 1.5rem 2rem; background: var(--panel-bg); border-bottom: var(--border-width) solid var(--panel-border);">
          <div style="flex: 1;">
              <select id="kam-selector" class="form-control" style="width: 300px; font-size: 1.1rem; padding: 0.75rem;">
                  <option value="ALL">Visualizando a todos los KAMs (Ver Todo)</option>
              </select>
          </div>
          <div style="font-size: 0.9rem; color: var(--text-muted); display: flex; gap: 1rem;">
              <span style="display: flex; align-items: center; gap: 4px;"><span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: var(--danger);"></span> Pelota en Cliente</span>
              <span style="display: flex; align-items: center; gap: 4px;"><span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: var(--warning);"></span> En Negociación</span>
              <span style="display: flex; align-items: center; gap: 4px;"><span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: var(--info);"></span> Pelota en Starken TI</span>
          </div>
      </div>
""", html, flags=re.DOTALL)

# Empty out view-pedidas because kam.js will rewrite it as cards
view_pedidas_target = r'<div class="table-container" id="view-pedidas">.*?</div>\s*(?=<!-- VISTA CLIENTES)'
view_pedidas_replacement = """
      <div id="view-alertas" style="padding: 2rem 2rem 0 2rem; display: none;">
          <h2 style="font-family: 'Playfair Display', serif; color: var(--danger); margin-bottom: 1rem; border-bottom: 1px solid var(--danger); padding-bottom: 0.5rem;">🔥 Alertas Comerciales Urgentes</h2>
          <div id="alertas-container" style="display: flex; flex-direction: column; gap: 1rem;"></div>
      </div>
      <div id="view-pedidas" style="padding: 2rem; display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 1.5rem;">
          <!-- Tarjetas KAM generadas por JS -->
      </div>
"""
html = re.sub(view_pedidas_target, view_pedidas_replacement, html, flags=re.DOTALL)

# Remove other views entirely
html = re.sub(r'<!-- VISTA CLIENTES -->.*?<!-- MODAL CLIENTE -->', '<!-- MODAL CLIENTE -->', html, flags=re.DOTALL)

# Re-design the Initiative Modal for KAMs
# KAMs only need to see the log history and add comments. No editing priority/phase.
modal_init_target = r'<div id="modal-initiative".*?</div>\s*</div>\s*</div>\s*(?=<!-- Fin Modal Initiative -->)'
modal_init_replacement = """
      <div id="modal-initiative" class="modal-overlay">
          <div class="modal-content" style="max-width: 700px;">
              <header class="header" style="justify-content: space-between; border-bottom: 1px solid var(--panel-border); margin-bottom: 1rem;">
                  <h2 id="modal-init-title" style="font-family: 'Playfair Display', serif; margin: 0;">Detalle de Iniciativa</h2>
                  <button type="button" class="btn-icon" id="btn-close-init-modal" style="border:none; background:transparent; font-size:1.5rem; cursor:pointer;">&times;</button>
              </header>
              <div class="form-section">
                  <div style="background: rgba(0,0,0,0.02); padding: 1rem; border-radius: 4px; border: 1px solid var(--panel-border); margin-bottom: 1.5rem;">
                      <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">ESTADO ACTUAL (Definido por PMO):</p>
                      <h3 id="kam-init-phase" style="margin: 0 0 0.5rem 0; color: var(--text-main);"></h3>
                      <p id="kam-init-bottleneck" style="color: var(--danger); margin: 0; font-size: 0.95rem;"></p>
                  </div>
                  
                  <h3 style="margin-top: 2rem; border-bottom: 1px solid var(--panel-border); padding-bottom: 0.5rem;">Bitácora Comercial / PMO</h3>
                  <div id="logs-container" style="max-height: 250px; overflow-y: auto; background: rgba(0,0,0,0.02); border: 1px solid var(--panel-border); border-radius: var(--radius); padding: 1rem; margin-top: 1rem; margin-bottom: 1rem; display: flex; flex-direction: column; gap: 0.75rem;">
                      <!-- Logs -->
                  </div>
                  
                  <div style="display: flex; gap: 10px; margin-top: 1rem;">
                      <input type="text" id="input-log-text" class="form-control" placeholder="Añadir respuesta, estado de negociación o update al PMO..." style="flex:1;">
                      <button type="button" id="btn-add-log" class="btn">Añadir Update</button>
                  </div>
              </div>
          </div>
      </div>
"""
html = re.sub(modal_init_target, modal_init_replacement, html, flags=re.DOTALL)


with open(kam_html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("kam.html generated successfully")
