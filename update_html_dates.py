import re

html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add Date fields to the initiative form
dates_html = r'''
            <div class="form-grid" style="margin-top: 1rem; border-top: 1px solid var(--panel-border); padding-top: 1rem;">
                <div class="form-group">
                    <label>Fecha Inicio</label>
                    <input type="date" id="input-init-start">
                </div>
                <div class="form-group">
                    <label>Fin Estimado</label>
                    <input type="date" id="input-init-est-end">
                </div>
                <div class="form-group">
                    <label>Fin Real</label>
                    <input type="date" id="input-init-act-end">
                </div>
            </div>
'''

target = r'(<div class="form-group full-width">\s*<label>Jira Link \(Opcional\)</label>\s*<input type="text" id="input-init-jira"[^>]*>\s*</div>\s*<div class="form-group full-width">\s*<label>Confluence Link \(Opcional\)</label>\s*<input type="text" id="input-init-confluence"[^>]*>\s*</div>)'
replacement = r'\1' + dates_html

html = re.sub(target, replacement, html)

# Change the table headers for the Pedidas view to match the new nested structure
table_target = r'(<table class="data-grid">\s*<thead>\s*<tr>\s*<th>Pri\.</th>\s*<th>Iniciativa</th>\s*<th>Tipo / Modelo</th>\s*<th>Esfuerzo / HH</th>\s*<th>Fase Actual</th>\s*<th>Responsable</th>\s*<th>Bloqueo / Cuello Botella</th>\s*<th>Acciones</th>\s*</tr>\s*</thead>\s*<tbody id="grid-body">\s*</tbody>\s*</table>)'
table_replacement = r'''<table class="data-grid" id="main-accordion-table">
              <thead>
                  <tr>
                      <th style="width: 40px;"></th>
                      <th>Cliente</th>
                      <th>Sponsor</th>
                      <th>Volumen / Mes</th>
                      <th>Total Pedidas</th>
                      <th>Estado General</th>
                  </tr>
              </thead>
              <tbody id="grid-body">
                  <!-- JS Inyecta el acordeón aquí -->
              </tbody>
          </table>'''
html = re.sub(table_target, table_replacement, html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html with dates and new table structure")
