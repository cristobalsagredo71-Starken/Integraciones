js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

switch_code = """
window.switchTab = (tabName) => {
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
    
    if(tabPedidas) tabPedidas.classList.remove('active');
    if(tabClientes) tabClientes.classList.remove('active');
    if(tabSistemas) tabSistemas.classList.remove('active');
    if(tabConductor) tabConductor.classList.remove('active');
    
    if(viewPedidas) viewPedidas.style.display = 'none';
    if(viewClientes) viewClientes.style.display = 'none';
    if(viewSistemas) viewSistemas.style.display = 'none';
    if(viewConductor) viewConductor.style.display = 'none';
    
    if(btnNewInit) btnNewInit.style.display = 'none';
    if(btnNewClient) btnNewClient.style.display = 'none';

    if (tabName === 'pedidas') {
        if(tabPedidas) tabPedidas.classList.add('active');
        if(viewPedidas) viewPedidas.style.display = 'block';
        if(btnNewInit) btnNewInit.style.display = 'inline-flex';
        renderGrid();
    } else if (tabName === 'clientes') {
        if(tabClientes) tabClientes.classList.add('active');
        if(viewClientes) viewClientes.style.display = 'block';
        if(btnNewClient) btnNewClient.style.display = 'inline-flex';
        renderClientsGrid();
    } else if (tabName === 'sistemas') {
        if(tabSistemas) tabSistemas.classList.add('active');
        if(viewSistemas) viewSistemas.style.display = 'block';
        if(btnNewClient) btnNewClient.style.display = 'inline-flex';
        renderSistemasGrid();
    } else if (tabName === 'conductor') {
        if(tabConductor) tabConductor.classList.add('active');
        if(viewConductor) viewConductor.style.display = 'block';
        renderConductorGrid();
    }
};
"""

target = "function renderClientsGrid() {"
js = js.replace(target, switch_code + "\n" + target)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Re-injected switchTab")
