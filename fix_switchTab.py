import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

new_switchTab = """window.switchTab = (tabName) => {
    const tabs = ['pedidas', 'clientes', 'sistemas', 'conductor', 'metricas'];
    tabs.forEach(t => {
        const btn = document.getElementById('tab-' + t);
        const view = document.getElementById('view-' + t);
        if (btn) btn.classList.remove('active');
        if (view) view.style.display = 'none';
    });

    const activeBtn = document.getElementById('tab-' + tabName);
    const activeView = document.getElementById('view-' + tabName);
    if (activeBtn) activeBtn.classList.add('active');
    if (activeView) activeView.style.display = 'block';

    const btnNewInit = document.getElementById('btn-new-initiative');
    const btnNewClient = document.getElementById('btn-new-client');
    if(btnNewInit) btnNewInit.style.display = 'none';
    if(btnNewClient) btnNewClient.style.display = 'none';

    if (tabName === 'pedidas') {
        if(btnNewInit) btnNewInit.style.display = 'inline-flex';
        renderGrid();
    } else if (tabName === 'clientes') {
        if(btnNewClient) btnNewClient.style.display = 'inline-flex';
        renderClientsGrid();
    } else if (tabName === 'sistemas') {
        renderSistemasGrid();
    } else if (tabName === 'conductor') {
        renderConductorGrid();
    } else if (tabName === 'metricas') {
        if (typeof renderCharts === 'function') renderCharts();
    }
};"""

# Replace the old switchTab
# The old switchTab ends just before `window.editClient =` or something similar.
js = re.sub(r'window\.switchTab = \(tabName\) => \{.*?\n\};\n', new_switchTab + '\n\n', js, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated switchTab")
