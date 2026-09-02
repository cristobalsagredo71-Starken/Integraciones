import re

content = open('app.js', 'r', encoding='utf-8').read()

pattern = r'function renderGrid\(\) \{[\s\S]*?window\.toggleAccordion = \(clientId, btnElement\) => \{[\s\S]*?\};'

replacement = """function renderGrid() {
    gridBody.innerHTML = '';
    let blockedCount = 0;

    const filtered = initiatives.filter(init => {
        const clientName = init.clients?.name || '';
        const clientSponsor = init.clients?.sponsor || '';
        const initName = init.name || '';
        const search = searchQuery.toLowerCase();
        return clientName.toLowerCase().includes(search) || 
               clientSponsor.toLowerCase().includes(search) ||
               initName.toLowerCase().includes(search);
    });

    if (filtered.length === 0 && initiatives.length > 0) {
        gridBody.innerHTML = '<tr><td colspan="8" style="text-align: center;">No hay resultados para tu búsqueda</td></tr>';
        return;
    }

    filtered.forEach(init => {
        const client = init.clients || {};
        
        if (init.phase === 'STANDBY' || init.bottleneck) blockedCount++;
        
        const priorityHtml = init.priority >= 4 
            ? `<span class="priority-badge p${init.priority}">P${init.priority}${init.priority === 5 ? ' 🔥' : ''}</span>`
            : (init.priority > 0 ? `<span class="priority-badge p${init.priority}">P${init.priority}</span>` : '-');

        let bottleneckHtml = '-';
        if (init.phase === 'STANDBY') {
            bottleneckHtml = `<span style="color: var(--danger)">🛑 Bloqueada: ${init.bottleneck || 'Sin motivo'}</span>`;
        } else if (init.bottleneck) {
            bottleneckHtml = `<span style="color: var(--warning)">⚠️ ${init.bottleneck}</span>`;
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="text-align: center;">${priorityHtml}</td>
            <td>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.2rem;">
                    ${client.name || 'Sin Cliente'} 
                    ${(client.tags || []).map(t => `<span class="badge-tag ${t.toLowerCase()}" style="transform: scale(0.8); display: inline-block;">${t}</span>`).join('')}
                </div>
                <strong style="font-size: 1.05rem;">${init.name}</strong>
                ${init.jira_link ? `<a href="${init.jira_link}" target="_blank" class="badge-tag" style="background: rgba(38, 132, 255, 0.2); color: #4c9aff; border: 1px solid rgba(38,132,255,0.4); text-decoration: none; margin-left: 5px;">Jira ↗</a>` : ''}
                ${init.attachments ? `<br><a href="${init.attachments}" target="_blank" style="font-size: 0.8rem; color: var(--info);">📎 Ver Documentación</a>` : ''}
            </td>
            <td>
                <span class="badge" style="background: rgba(255,255,255,0.1)">${init.type || '-'}</span><br>
                <small style="color: var(--text-muted)">${init.model || '-'}</small>
            </td>
            <td>
                <div><strong style="color: var(--info)">${init.hh || 0} HH</strong></div>
                <div style="font-size: 0.8rem; color: var(--text-muted)">Dif: ${init.complexity || '-'}</div>
            </td>
            <td>
                <span class="badge badge-phase-${(init.phase || '').toLowerCase()}">${init.phase || '-'}</span>
            </td>
            <td>
                <span style="font-weight: 600" class="owner-${init.owner || ''}">${init.owner || '-'}</span>
            </td>
            <td>
                ${bottleneckHtml}
            </td>
            <td style="display: flex; gap: 0.25rem;">
                <button class="btn-icon tooltip-container" onclick="editInitiative('${init.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Editar Pedida</div>
                </button>
                <button class="btn-icon danger tooltip-container" onclick="deleteInitiative('${init.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                    <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Borrar Pedida</div>
                </button>
            </td>
        `;
        gridBody.appendChild(tr);
    });

    elTotal.textContent = filtered.length;
    elBlocked.textContent = blockedCount;
}
"""

new_content = re.sub(pattern, replacement, content)
open('app.js', 'w', encoding='utf-8').write(new_content)
print('Done flattening grid')
