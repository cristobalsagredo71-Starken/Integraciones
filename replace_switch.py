js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

start_idx = js.find("window.switchTab = (tab) => {")
end_idx = js.find("function renderClientsGrid() {")

if start_idx != -1 and end_idx != -1:
    new_switch_tab = """window.switchTab = (tabName) => {
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
        btnNewClient.style.display = 'inline-flex';
        renderSistemasGrid();
    } else if (tabName === 'conductor') {
        tabConductor.classList.add('active');
        viewConductor.style.display = 'block';
        renderConductorGrid();
    }
};

"""
    js = js[:start_idx] + new_switch_tab + js[end_idx:]
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced window.switchTab successfully!")
else:
    print("Could not find boundaries")
