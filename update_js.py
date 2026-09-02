import re

content = open('app.js', 'r', encoding='utf-8').read()

# 1. Add global variable and fetch logic
fetch_logic = """
let clientFlows = {};

async function fetchFlows() {
    try {
        const res = await fetch('flows.json');
        if (res.ok) {
            clientFlows = await res.json();
        }
    } catch (e) {
        console.log("No se pudo cargar flows.json", e);
    }
}
"""
content = re.sub(r'(let clientsData = \[\];)', r'\1\n' + fetch_logic, content)

# Update init to also fetchFlows
content = content.replace("fetchClients().then(() => fetchInitiatives());", "fetchFlows().then(() => fetchClients()).then(() => fetchInitiatives());")


# Helper to generate details HTML
helper = """
function getFlowsHtml(clientName) {
    const flows = clientFlows[clientName];
    if (!flows || flows.length === 0) return '';
    
    let linksHtml = flows.map(f => `<a href="${f.url}" target="_blank" class="badge-tag" style="display: block; margin-top: 4px; background: rgba(255,255,255,0.1); color: var(--text-primary); text-decoration: none; border: 1px solid rgba(255,255,255,0.2);">📄 ${f.name}</a>`).join('');
    
    return `
    <details style="margin-top: 5px;">
        <summary class="badge-tag" style="cursor:pointer; background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); user-select: none;">🖥️ Flujos (${flows.length}) ▼</summary>
        <div style="padding-left: 5px;">${linksHtml}</div>
    </details>`;
}
"""
content = re.sub(r'(function renderGrid\(\) {)', helper + r'\n\1', content)


# Inject into renderGrid
target_grid = r'<div style="font-size: 0.8rem; color: var\(--text-muted\); margin-bottom: 0\.2rem;">\s*\$\{client\.name \|\| \'Sin Cliente\'\}\s*</div>'
replacement_grid = r"""<div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.2rem; display: flex; align-items: center; gap: 8px;">
                      <span>${client.name || 'Sin Cliente'}</span>
                      ${getFlowsHtml(client.name)}
                  </div>"""
content = re.sub(target_grid, replacement_grid, content)

# Inject into renderClientsGrid
target_clients = r'<strong>\$\{clientData\.name\}</strong>'
replacement_clients = r'<strong>${clientData.name}</strong> ${getFlowsHtml(clientData.name)}'
content = re.sub(target_clients, replacement_clients, content)

open('app.js', 'w', encoding='utf-8').write(content)
print("Updated app.js with flows.json logic")
