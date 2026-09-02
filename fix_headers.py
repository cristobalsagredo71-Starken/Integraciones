import re

html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

target = r'<table class="data-grid">\s*<thead>\s*<tr>\s*<th>Pri\.</th>\s*<th>Iniciativa</th>\s*<th>Tipo / Modelo</th>\s*<th>Esfuerzo / HH</th>\s*<th>Fase Actual</th>\s*<th>Responsable</th>\s*<th>Bloqueo / Cuello Botella</th>\s*<th>Acciones</th>\s*</tr>\s*</thead>\s*<tbody id="grid-body">\s*<!-- Filas generadas por JS -->\s*</tbody>\s*</table>'

replacement = r'''<table class="data-grid" id="main-accordion-table" style="table-layout: fixed; width: 100%;">
                    <thead>
                    <tr>
                        <th style="width: 50px; text-align: center;"></th>
                        <th style="width: 20%;">Cliente</th>
                        <th style="width: 20%;">Sponsor (KAM)</th>
                        <th style="width: 20%;">Volumen / Fac.</th>
                        <th style="width: 15%;">Resumen Pedidas</th>
                        <th style="width: 20%;">Estado de Salud</th>
                    </tr>
                    </thead>
                    <tbody id="grid-body">
                        <!-- JS Inyecta el acordeón aquí -->
                    </tbody>
                </table>'''

# Use search to find exactly what to replace if regex is stubborn
start_idx = html.find('<table class="data-grid">')
if start_idx != -1:
    end_idx = html.find('</table>', start_idx) + 8
    
    # Ensure we are replacing the FIRST table (view-pedidas)
    old_table = html[start_idx:end_idx]
    if "Pri." in old_table and "grid-body" in old_table:
        html = html[:start_idx] + replacement + html[end_idx:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed table headers")
