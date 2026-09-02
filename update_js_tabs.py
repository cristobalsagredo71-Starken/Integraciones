import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Add DOM Elements for Tabs
dom_target = r'const btnNewClient = document\.getElementById\(\'btn-new-client\'\);'
dom_replacement = dom_target + r'''
const tabSistemas = document.getElementById('tab-sistemas');
const tabConductor = document.getElementById('tab-conductor');
const viewSistemas = document.getElementById('view-sistemas');
const viewConductor = document.getElementById('view-conductor');
const conductorGrid = document.getElementById('conductor-grid');
'''
js = re.sub(dom_target, dom_replacement, js)

# Switch Tab Logic
switch_target = r'function switchTab\(tabName\) \{.*?\}\s*\}'
switch_replacement = r'''window.switchTab = function(tabName) {
    tabPedidas.classList.remove('active');
    tabClientes.classList.remove('active');
    tabSistemas.classList.remove('active');
    tabConductor.classList.remove('active');
    
    viewPedidas.style.display = 'none';
    viewClientes.style.display = 'none';
    viewSistemas.style.display = 'none';
    viewConductor.style.display = 'none';
    
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
        // renderSistemasGrid() to be implemented based on user feedback
    } else if (tabName === 'conductor') {
        tabConductor.classList.add('active');
        viewConductor.style.display = 'block';
        renderConductorGrid();
    }
};'''
js = re.sub(switch_target, switch_replacement, js, flags=re.DOTALL)

# Conductor Grid Render
conductor_render = r'''
function renderConductorGrid() {
    conductorGrid.innerHTML = '';
    const flows = clientFlows["Conductor Regular"] || [];
    
    if (flows.length === 0) {
        conductorGrid.innerHTML = '<p style="color: var(--text-muted); grid-column: 1 / -1;">No hay flujos subidos al Conductor Regular todavía.</p>';
        return;
    }
    
    flows.forEach(f => {
        const card = document.createElement('a');
        card.href = f.url;
        card.target = '_blank';
        card.style = `
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 1rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            text-decoration: none;
            color: var(--text-primary);
            transition: all 0.2s;
            cursor: pointer;
        `;
        card.onmouseover = () => { card.style.borderColor = 'var(--primary)'; card.style.transform = 'translateY(-2px)'; };
        card.onmouseout = () => { card.style.borderColor = 'var(--border-color)'; card.style.transform = 'none'; };
        
        card.innerHTML = `
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" style="margin-bottom: 1rem;">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <strong style="text-align: center;">${f.name}</strong>
        `;
        conductorGrid.appendChild(card);
    });
}
'''
js = js + conductor_render

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated app.js logic")
