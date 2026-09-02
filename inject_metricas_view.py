import re

html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

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
        </div>\n        <div id="view-conductor" """

html = re.sub(r'<div id="view-conductor" ', view_replacement, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Injected view-metricas")
