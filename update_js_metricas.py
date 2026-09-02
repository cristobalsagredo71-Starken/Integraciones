import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update switchTab array
if "'metricas'" not in js:
    js = js.replace("['pedidas', 'clientes', 'sistemas', 'conductor']", "['pedidas', 'clientes', 'sistemas', 'conductor', 'metricas']")

# 2. Append Chart JS logic
chart_logic = """
// Chart logic
let chartRevenueInstance = null;
let chartVolumeInstance = null;

function renderCharts() {
    const ctxRev = document.getElementById('chartRevenue');
    const ctxVol = document.getElementById('chartVolume');
    if (!ctxRev || !ctxVol) return;

    const sortedByRevenue = [...clients].filter(c => c.revenue > 0).sort((a,b) => b.revenue - a.revenue);
    const sortedByVolume = [...clients].filter(c => c.volume > 0).sort((a,b) => b.volume - a.volume);

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
                backgroundColor: 'rgba(29, 78, 216, 0.7)', // Cobalt Blue WSJ
                borderColor: 'rgba(29, 78, 216, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
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
                backgroundColor: 'rgba(21, 128, 61, 0.7)', // Emerald Green
                borderColor: 'rgba(21, 128, 61, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { grid: { color: gridColor }, ticks: { callback: (val) => (val/1000).toFixed(0) + 'k' } },
                x: { grid: { display: false } }
            },
            plugins: {
                tooltip: { callbacks: { label: (ctx) => ' ' + ctx.raw.toLocaleString('es-CL') + ' OFs' } }
            }
        }
    });
}
"""

if "function renderCharts()" not in js:
    js += chart_logic
    # Call renderCharts() after loading data
    js = js.replace("renderConductorGrid();", "renderConductorGrid();\n        renderCharts();")
    
    # Update toggleTheme to re-render charts so colors update
    js = js.replace("localStorage.setItem('theme', newTheme);", "localStorage.setItem('theme', newTheme);\n    if (typeof renderCharts === 'function') renderCharts();")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("JS updated with Metricas logic")
