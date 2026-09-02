import re
js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Fix broken DOM queries
js = js.replace(r"document\.getElementById\(\'btn-new-client\'\)", "document.getElementById('btn-new-client')")

# Fix switchTab
switch_target = r'window\.switchTab = \(tab\) => \{.*?\};\s*\}'
switch_replacement = r'''window.switchTab = (tabName) => {
    const tabPedidas = document.getElementById('tab-pedidas');
    const tabClientes = document.getElementById('tab-clientes');
    const tabSistemas = document.getElementById('tab-sistemas');
    const tabConductor = document.getElementById('tab-conductor');
    
    const viewPedidas = document.getElementById('view-pedidas');
    const viewClientes = document.getElementById('view-clientes');
    const viewSistemas = document.getElementById('view-sistemas');
    const viewConductor = document.getElementById('view-conductor');
    
    const btnNewInit = document.getElementById('btn-new-initiative');
    const btnNewClient = document.getElementById('btn-new-client');
    
    [tabPedidas, tabClientes, tabSistemas, tabConductor].forEach(t => t.classList.remove('active'));
    [viewPedidas, viewClientes, viewSistemas, viewConductor].forEach(v => v.style.display = 'none');
    btnNewInit.style.display = 'none';
    btnNewClient.style.display = 'none';

    if (tabName === 'pedidas') {
        tabPedidas.classList.add('active');
        viewPedidas.style.display = 'block';
        btnNewInit.style.display = 'inline-flex';
        renderGrid();
    } else if (tabName === 'clientes') {
        tabClientes.classList.add('active');
        viewClientes.style.display = 'block';
        btnNewClient.style.display = 'inline-flex';
        renderClientsGrid();
    } else if (tabName === 'sistemas') {
        tabSistemas.classList.add('active');
        viewSistemas.style.display = 'block';
        btnNewClient.style.display = "inline-flex";
        renderSistemasGrid();
    } else if (tabName === 'conductor') {
        tabConductor.classList.add('active');
        viewConductor.style.display = 'block';
        renderConductorGrid();
    }
};'''
js = re.sub(switch_target, switch_replacement, js, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Repaired app.js syntax")
