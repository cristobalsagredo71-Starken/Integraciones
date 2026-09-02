import re

html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Chart.js to head
if "chart.js" not in html:
    html = html.replace('</head>', '    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>')

# 2. Add Tab Button
tab_target = '<button class="tab-btn" onclick="switchTab(\'conductor\')" id="tab-conductor">Conductor Regular</button>'
tab_replacement = tab_target + '\n        <button class="tab-btn" onclick="switchTab(\'metricas\')" id="tab-metricas">Métricas</button>'
if "id=\"tab-metricas\"" not in html:
    html = html.replace(tab_target, tab_replacement)

# 3. Add View Container
view_target = '<div class="table-container" id="view-conductor" style="display: none;">'
view_replacement = """<div class="table-container" id="view-metricas" style="display: none; padding: 2rem;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;">
                <div>
                    <h3 style="font-family: 'Playfair Display', serif; margin-bottom: 1.5rem; color: var(--text-main); border-bottom: 1px dashed var(--panel-border); padding-bottom: 0.5rem;">Facturación Promedio por Cliente</h3>
                    <canvas id="chartRevenue"></canvas>
                </div>
                <div>
                    <h3 style="font-family: 'Playfair Display', serif; margin-bottom: 1.5rem; color: var(--text-main); border-bottom: 1px dashed var(--panel-border); padding-bottom: 0.5rem;">Volumen (OFs) por Cliente</h3>
                    <canvas id="chartVolume"></canvas>
                </div>
            </div>
        </div>\n        """ + view_target
if "id=\"view-metricas\"" not in html:
    html = html.replace(view_target, view_replacement)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML updated with Metricas tab")
