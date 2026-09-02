import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update form submission to include dates
submit_target = r'confluence_link:\s*document\.getElementById\(\'input-init-confluence\'\)\.value,'
submit_replacement = r'''confluence_link: document.getElementById('input-init-confluence').value,
            start_date: document.getElementById('input-init-start').value || null,
            estimated_end_date: document.getElementById('input-init-est-end').value || null,
            actual_end_date: document.getElementById('input-init-act-end').value || null,'''
js = re.sub(submit_target, submit_replacement, js)

# 2. Update form population to load dates
load_target = r'document\.getElementById\(\'input-init-confluence\'\)\.value\s*=\s*init\.confluence_link\s*\|\|\s*\'\';'
load_replacement = r'''document.getElementById('input-init-confluence').value = init.confluence_link || '';
        document.getElementById('input-init-start').value = init.start_date || '';
        document.getElementById('input-init-est-end').value = init.estimated_end_date || '';
        document.getElementById('input-init-act-end').value = init.actual_end_date || '';'''
js = re.sub(load_target, load_replacement, js)

# 3. Update reset form
reset_target = r'document\.getElementById\(\'input-init-confluence\'\)\.value\s*=\s*\'\';'
reset_replacement = r'''document.getElementById('input-init-confluence').value = '';
        document.getElementById('input-init-start').value = '';
        document.getElementById('input-init-est-end').value = '';
        document.getElementById('input-init-act-end').value = '';'''
js = re.sub(reset_target, reset_replacement, js)

# 4. Rewrite renderGrid
render_target = r'function renderGrid\(\) \{.*?(?=function renderClientsGrid\(\) \{)'
new_render = r'''
window.toggleAccordion = function(clientId) {
    const row = document.getElementById(`nested-${clientId}`);
    const icon = document.getElementById(`icon-${clientId}`);
    if (row.style.display === 'none') {
        row.style.display = 'table-row';
        icon.style.transform = 'rotate(90deg)';
    } else {
        row.style.display = 'none';
        icon.style.transform = 'rotate(0deg)';
    }
};

function formatDate(dateStr) {
    if (!dateStr) return '-';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year.substring(2)}`;
}

function renderGrid() {
    gridBody.innerHTML = '';
    let blockedCount = 0;

    const filteredInits = initiatives.filter(init => {
        const clientName = init.clients?.name || '';
        const clientSponsor = init.clients?.sponsor || '';
        const initName = init.name || '';
        const search = searchQuery.toLowerCase();
        return clientName.toLowerCase().includes(search) || 
               clientSponsor.toLowerCase().includes(search) ||
               initName.toLowerCase().includes(search);
    });

    if (filteredInits.length === 0 && initiatives.length > 0) {
        gridBody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No hay resultados para tu búsqueda</td></tr>';
        return;
    }
    
    // Group filtered initiatives by client
    const grouped = {};
    const unassigned = [];
    
    filteredInits.forEach(init => {
        if (init.phase === 'STANDBY' || init.bottleneck) blockedCount++;
        
        if (init.client_id && init.clients) {
            if (!grouped[init.client_id]) grouped[init.client_id] = { client: init.clients, inits: [] };
            grouped[init.client_id].inits.push(init);
        } else {
            unassigned.push(init);
        }
    });
    
    // Sort clients by priority of their highest initiative
    const sortedClientIds = Object.keys(grouped).sort((a, b) => {
        const maxA = Math.max(...grouped[a].inits.map(i => i.priority));
        const maxB = Math.max(...grouped[b].inits.map(i => i.priority));
        return maxB - maxA;
    });

    const renderInitRow = (init) => {
        const priorityHtml = init.priority >= 4 
            ? `<span class="priority-badge p${init.priority}">P${init.priority}${init.priority === 5 ? ' 🔥' : ''}</span>`
            : (init.priority > 0 ? `<span class="priority-badge p${init.priority}">P${init.priority}</span>` : '-');

        let bottleneckHtml = '-';
        if (init.phase === 'STANDBY') {
            bottleneckHtml = `<span style="color: var(--danger)">🛑 Bloqueada: ${init.bottleneck || 'Sin motivo'}</span>`;
        } else if (init.bottleneck) {
            bottleneckHtml = `<span style="color: var(--warning)">⚠️ ${init.bottleneck}</span>`;
        }
        
        const datesHtml = `
            <div style="font-size: 0.8rem; color: var(--text-muted); display: grid; grid-template-columns: auto 1fr; gap: 4px;">
                <span>Inicio:</span> <span style="color: white;">${formatDate(init.start_date)}</span>
                <span>Fin Est.:</span> <span style="color: var(--info);">${formatDate(init.estimated_end_date)}</span>
            </div>
        `;

        return `
            <tr>
                <td style="text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);">${priorityHtml}</td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <strong style="font-size: 1.05rem;">${init.name}</strong> ${getFlowsHtml(init.name)}
                    ${init.jira_url ? `<br><a href="${init.jira_url}" target="_blank" class="badge-tag" style="background: rgba(38, 132, 255, 0.2); color: #4c9aff; border: 1px solid rgba(38,132,255,0.4); text-decoration: none; margin-top: 4px; display: inline-block;">Jira ↗</a>` : ''}
                    ${init.confluence_link ? `<a href="${init.confluence_link}" target="_blank" class="badge-tag" style="background: rgba(0, 184, 217, 0.2); color: #00b8d9; border: 1px solid rgba(0, 184, 217, 0.4); text-decoration: none; margin-top: 4px; display: inline-block; margin-left: 4px;">Confluence ↗</a>` : ''}
                </td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <span class="badge" style="background: rgba(255,255,255,0.1)">${init.type}</span>
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">${init.model}</div>
                </td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <div><strong>${init.hh} HH</strong></div>
                    <div style="font-size: 0.8rem; color: var(--text-muted)">Dif: ${init.difficulty}</div>
                </td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <span class="phase-badge phase-${init.phase}">${init.phase}</span><br>
                    <span class="owner-badge owner-${init.owner.replace(/[^a-zA-Z]/g, '')}" style="margin-top: 4px; display: inline-block;">${init.owner}</span>
                </td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">${datesHtml}</td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">${bottleneckHtml}</td>
                <td style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <button class="btn-icon tooltip-container" onclick="editInitiative('${init.id}')">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                        <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Editar Pedida</div>
                    </button>
                </td>
            </tr>
        `;
    };

    // Render Grouped
    sortedClientIds.forEach(clientId => {
        const { client, inits } = grouped[clientId];
        const hasBlocked = inits.some(i => i.phase === 'STANDBY' || i.bottleneck);
        const maxPriority = Math.max(...inits.map(i => i.priority));
        
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.style.background = 'rgba(255,255,255,0.02)';
        tr.onclick = () => toggleAccordion(clientId);
        tr.innerHTML = `
            <td style="text-align: center;">
                <svg id="icon-${clientId}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="2" style="transition: transform 0.2s;"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </td>
            <td>
                <strong style="font-size: 1.1rem; color: var(--text-main);">${client.name}</strong>
                <span class="tags-container" style="margin-left: 8px;">${(client.tags || []).map(t => `<span class="badge-tag ${t.toLowerCase()}" style="transform: scale(0.8); display: inline-block;">${t}</span>`).join('')}</span>
            </td>
            <td>${client.sponsor || '-'}</td>
            <td>
                <div>${formatNumber(client.volume)} OFs</div>
                <div style="font-size: 0.8rem; color: var(--text-muted)">${formatMoney(client.revenue)}</div>
            </td>
            <td>
                <span class="badge" style="background: rgba(255,255,255,0.1)">${inits.length} Pedidas</span>
                ${maxPriority >= 4 ? `<span style="font-size: 0.8rem; color: var(--danger); margin-left: 4px;">(P${maxPriority})</span>` : ''}
            </td>
            <td>
                ${hasBlocked ? `<span style="color: var(--danger); font-size: 0.9rem;">⚠️ Hay Bloqueos</span>` : `<span style="color: var(--info); font-size: 0.9rem;">✅ Sano</span>`}
            </td>
        `;
        gridBody.appendChild(tr);

        // Nested Row
        const nestedTr = document.createElement('tr');
        nestedTr.id = `nested-${clientId}`;
        nestedTr.style.display = 'none'; // Default collapsed
        
        const innerTableHtml = `
            <td colspan="6" style="padding: 0; background: rgba(0,0,0,0.2);">
                <div style="padding: 1rem 1rem 1rem 3rem;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem; width: 50px;">Pri.</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Iniciativa</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Tipo/Modelo</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Esfuerzo</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Fase/Resp.</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Tiempos</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Bloqueos</th>
                                <th style="text-align: left; padding: 0.5rem; color: var(--text-muted); font-size: 0.8rem;">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${inits.sort((a, b) => b.priority - a.priority).map(renderInitRow).join('')}
                        </tbody>
                    </table>
                </div>
            </td>
        `;
        nestedTr.innerHTML = innerTableHtml;
        gridBody.appendChild(nestedTr);
    });

    elTotal.textContent = filteredInits.length;
    elBlocked.textContent = blockedCount;
}
'''
js = re.sub(render_target, new_render, js, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS with Accordion renderGrid")
