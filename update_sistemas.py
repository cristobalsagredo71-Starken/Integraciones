import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Add view container for Sistemas in index.html (I'll do it via HTML update later, I'll just write the JS render function here)

render_sistemas = r'''
function renderSistemasGrid() {
    const viewSistemas = document.getElementById('view-sistemas');
    // Clear everything except the title
    viewSistemas.innerHTML = '<h2 style="color: var(--text-primary); margin-bottom: 1rem;">Sistemas y Ecosistema</h2><div id="sistemas-container"></div>';
    const container = document.getElementById('sistemas-container');
    
    // Find all unique tags
    const allTags = new Set();
    clientsData.forEach(c => {
        (c.tags || []).forEach(t => allTags.add(t));
    });
    
    if (allTags.size === 0) {
        container.innerHTML = '<div class="panel"><p style="color: var(--text-muted); text-align: center; padding: 2rem;">No hay clientes con sistemas (tags) asignados.</p></div>';
        return;
    }
    
    // Convert to sorted array
    const sortedTags = Array.from(allTags).sort();
    
    sortedTags.forEach(tag => {
        const clientsWithTag = clientsData.filter(c => (c.tags || []).includes(tag));
        
        const section = document.createElement('div');
        section.className = 'panel';
        section.style.marginBottom = '2rem';
        
        // Header of the section
        const header = document.createElement('div');
        header.style.padding = '1rem 1.5rem';
        header.style.borderBottom = '1px solid var(--border-color)';
        header.innerHTML = `<h3 style="margin:0;"><span class="badge-tag ${tag.toLowerCase()}">${tag}</span> <span style="font-size: 0.9rem; color: var(--text-muted); font-weight: normal;">(${clientsWithTag.length} Clientes)</span></h3>`;
        section.appendChild(header);
        
        // Table of clients
        const table = document.createElement('table');
        table.className = 'table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Cliente</th>
                    <th>Sponsor</th>
                    <th>Volumen / Mes</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                ${clientsWithTag.map(c => `
                    <tr>
                        <td><strong>${c.name}</strong> ${getFlowsHtml(c.name)}</td>
                        <td>${c.sponsor || '-'}</td>
                        <td>
                            <div>${formatNumber(c.volume)} OFs</div>
                            <div style="font-size: 0.8rem; color: var(--text-muted)">${formatMoney(c.revenue)}</div>
                        </td>
                        <td>
                            <button class="btn-icon tooltip-container" style="margin-right: 0.5rem;" onclick="editClient('${c.id}')">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                                <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Editar Cliente</div>
                            </button>
                            <button class="btn-icon danger tooltip-container" onclick="deleteClientSoft('${c.id}')">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                                <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Borrar Cliente</div>
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        section.appendChild(table);
        container.appendChild(section);
    });
}
'''
js = js + render_sistemas

# Update the switchTab to call renderSistemasGrid
js = js.replace('// renderSistemasGrid() to be implemented based on user feedback', 'renderSistemasGrid(); btnNewClient.style.display = "inline-flex";')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS with renderSistemasGrid")
