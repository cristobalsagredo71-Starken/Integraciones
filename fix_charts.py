import re
js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

new_renderCharts = """function renderCharts() {
    try {
        const ctxRev = document.getElementById('chartRevenue');
        const ctxVol = document.getElementById('chartVolume');
        if (!ctxRev || !ctxVol) return;

        // Force parent heights
        ctxRev.parentElement.style.position = 'relative';
        ctxRev.parentElement.style.height = '400px';
        ctxVol.parentElement.style.position = 'relative';
        ctxVol.parentElement.style.height = '400px';

        const sortedByRevenue = [...clients].filter(c => c.revenue > 0).sort((a,b) => b.revenue - a.revenue);
        const sortedByVolume = [...clients].filter(c => c.volume > 0).sort((a,b) => b.volume - a.volume);

        if (!window.Chart) {
            ctxRev.parentElement.innerHTML += '<p style="color:red">Error: Chart.js no cargó.</p>';
            return;
        }

        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        Chart.defaults.color = isDark ? '#a1a1aa' : '#6b7280';
        Chart.defaults.font.family = "'Inter', sans-serif";
        const gridColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';

        if (chartRevenueInstance) chartRevenueInstance.destroy();
        chartRevenueInstance = new Chart(ctxRev, {
            type: 'bar',
            data: {
                labels: sortedByRevenue.map(c => c.name),
                datasets: [{
                    label: 'Facturación ($)',
                    data: sortedByRevenue.map(c => c.revenue),
                    backgroundColor: 'rgba(29, 78, 216, 0.7)',
                    borderColor: 'rgba(29, 78, 216, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: gridColor }, ticks: { callback: (val) => '$' + (val/1000000).toFixed(1) + 'M' } },
                    x: { grid: { display: false } }
                },
                plugins: {
                    tooltip: { callbacks: { label: (ctx) => ' $' + ctx.raw.toLocaleString('es-CL') } }
                }
            }
        });

        if (chartVolumeInstance) chartVolumeInstance.destroy();
        chartVolumeInstance = new Chart(ctxVol, {
            type: 'bar',
            data: {
                labels: sortedByVolume.map(c => c.name),
                datasets: [{
                    label: 'Volumen (OFs)',
                    data: sortedByVolume.map(c => c.volume),
                    backgroundColor: 'rgba(21, 128, 61, 0.7)',
                    borderColor: 'rgba(21, 128, 61, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: gridColor }, ticks: { callback: (val) => (val/1000).toFixed(0) + 'k' } },
                    x: { grid: { display: false } }
                },
                plugins: {
                    tooltip: { callbacks: { label: (ctx) => ' ' + ctx.raw.toLocaleString('es-CL') + ' OFs' } }
                }
            }
        });
    } catch (e) {
        document.getElementById('view-metricas').innerHTML += `<p style="color:red">Error JS: ${e.message}</p>`;
    }
}"""

js = re.sub(r'function renderCharts\(\) \{.*?(?=\n\n|\Z)', new_renderCharts, js, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated renderCharts logic")
