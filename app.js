// --- CONFIGURACIÓN SUPABASE ---
// ðŸš¨ IMPORTANTE: REEMPLAZA "TU_API_KEY_AQUI" CON TU CLAVE "anon public" ðŸš¨
const SUPABASE_URL = 'https://dzmsfxnvfardckddvzjt.supabase.co';
const SUPABASE_KEY = 'sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN';

const client = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// State
let initiatives = [];
let clientsData = [];

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

let editingId = null;
let searchQuery = "";
let currentHistory = [];

// DOM Elements
const gridBody = document.getElementById('grid-body');
const modalClient = document.getElementById('modal-client');
const modalInit = document.getElementById('modal-initiative');
const btnNewInit = document.getElementById('btn-new-initiative');
const btnNewClient = document.getElementById('btn-new-client');
const tabSistemas = document.getElementById('tab-sistemas');
const tabConductor = document.getElementById('tab-conductor');
const viewSistemas = document.getElementById('view-sistemas');
const viewConductor = document.getElementById('view-conductor');
const conductorGrid = document.getElementById('conductor-grid');

const btnCloseClient = document.getElementById('btn-close-client-modal');
const btnCloseInit = document.getElementById('btn-close-init-modal');
const btnCancelClient = document.getElementById('btn-cancel-client');
const btnCancelInit = document.getElementById('btn-cancel-init');
const formInit = document.getElementById('initiative-form');
const formClient = document.getElementById('client-form');
const searchInput = document.getElementById('search-input');
const elTotal = document.getElementById('total-integrations');
const elBlocked = document.getElementById('total-blocked');

// Formatters
const formatMoney = (amount) => new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' }).format(amount || 0);
const formatNumber = (num) => new Intl.NumberFormat('es-CL').format(num || 0);

// Helper para renderizar multiples archivos
function renderAttachments(attachmentsStr) {
    if (!attachmentsStr) return '';
    try {
        const arr = JSON.parse(attachmentsStr);
        if (Array.isArray(arr)) {
            return arr.map((url, i) => `<a href="${url}" target="_blank" style="color: var(--info); font-size: 0.8rem; margin-right: 0.5rem; display: inline-block;">ðŸ“Ž Archivo ${i}</a>`).join('');
        }
        return `<a href="${attachmentsStr}" target="_blank" style="color: var(--info); font-size: 0.8rem;">ðŸ“Ž Archivo</a>`;
    } catch (e) {
        return `<a href="${attachmentsStr}" target="_blank" style="color: var(--info); font-size: 0.8rem;">ðŸ“Ž Archivo</a>`;
    }
}


// --- OPERACIONES BASE DE DATOS ---

async function fetchClients() {
    try {
        const { data, error } = await client
            .from('clients')
            .select('*')
            .is('deleted_at', null)
            .order('name', { ascending: true });
        
        if (error) throw error;
        clientsData = data || [];
        renderClientSelect();
    } catch (err) {
        console.error("Error cargando clientes:", err.message);
    }
}

function renderClientSelect() {
    const select = document.getElementById('input-init-client-select');
    select.innerHTML = '<option value="">-- Selecciona un cliente --</option>';
    clientsData.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.id;
        opt.textContent = c.name;
        select.appendChild(opt);
    });
}


async function fetchInitiatives() {
    try {
        gridBody.innerHTML = '<tr><td colspan="7" style="text-align: center;">Cargando datos desde Supabase...</td></tr>';

        if (SUPABASE_KEY === 'TU_API_KEY_AQUI') {
            throw new Error("Falta configurar la API Key de Supabase en app.js");
        }

        const { data, error } = await client
            .from('initiatives')
            .select('*, clients(*)')
            .is('deleted_at', null)
            .order('priority', { ascending: false })
            .order('created_at', { ascending: false });

        if (error) throw error;
        initiatives = data || [];
        renderGrid();
    } catch (err) {
        console.error("Error cargando datos:", err.message);
        gridBody.innerHTML = `<tr><td colspan="7" style="color: var(--danger); text-align: center;">Error de ConexiÃ³n: ${err.message}. AsegÃºrate de poner tu API Key en app.js y crear la tabla en Supabase.</td></tr>`;
    }
}

async function uploadFileToSupabase(file, bucketName) {
    const fileExt = file.name.split('.').pop();
    const fileName = `${Math.random().toString(36).substring(2)}_${Date.now()}.${fileExt}`;
    const filePath = `${fileName}`;

    const { error: uploadError } = await client.storage.from(bucketName).upload(filePath, file);
    if (uploadError) throw uploadError;

    const { data } = client.storage.from(bucketName).getPublicUrl(filePath);
    return data.publicUrl;
}


// --- RENDERIZADO UI ---



function getFlowsHtml(clientName) {
    const flows = clientFlows[clientName];
    if (!flows || flows.length === 0) return '';
    
    return `<span onclick="openFlowsModal('${clientName}')" class="tooltip-container" style="cursor:pointer; color: #10b981; font-size: 1.1rem; display: inline-flex; align-items: center; margin-left: 2px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 2px;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        <span style="font-size: 0.75rem; font-weight: bold;">${flows.length}</span>
        <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Ver ${flows.length} Flujos</div>
    </span>`;
}

function openFlowsModal(clientName) {
    const flows = clientFlows[clientName];
    if (!flows || flows.length === 0) return;
    
    // Remove existing modal if any
    const existing = document.getElementById('dynamic-flows-modal');
    if (existing) existing.remove();
    
    let linksHtml = flows.map(f => `<a href="${f.url}" target="_blank" class="badge-tag" style="display: block; padding: 12px; margin-bottom: 8px; background: rgba(255,255,255,0.05); color: var(--text-primary); text-decoration: none; border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; font-size: 0.9rem; text-align: center;">📄 ${f.name}</a>`).join('');
    
    const modalHtml = `
    <div id="dynamic-flows-modal" class="modal-overlay active" style="z-index: 9999;">
        <div class="modal-content" style="max-width: 400px; text-align: center;">
            <div class="modal-header">
                <h2>Flujos: ${clientName}</h2>
                <button class="close-btn" onclick="document.getElementById('dynamic-flows-modal').remove()">&times;</button>
            </div>
            <div style="padding: 20px 0;">
                ${linksHtml}
            </div>
        </div>
    </div>`;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}



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

    
window.toggleBitacora = (id) => {
    const el = document.getElementById('bitacora-' + id);
    if (el) {
        el.style.display = el.style.display === 'none' ? 'table-row' : 'none';
    }
};
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
                    ${(init.logs && init.logs.length > 0) ? `<button type="button" onclick="event.stopPropagation(); toggleBitacora('${init.id}')" class="badge-tag" style="background: rgba(107, 114, 128, 0.2); color: var(--text-muted); border: 1px solid rgba(107, 114, 128, 0.4); text-decoration: none; margin-top: 4px; display: inline-block; margin-left: 4px; cursor: pointer;">Bitácora (${init.logs.length}) 📖</button>` : ''}
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
            ${(init.logs && init.logs.length > 0) ? `
            <tr id="bitacora-${init.id}" style="display: none; background: var(--bg-color);">
                <td colspan="8" style="padding: 1rem 1rem 1rem 3rem; border-bottom: 1px solid var(--panel-border);">
                    <div style="font-size: 0.75rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; margin-bottom: 0.5rem; border-bottom: 1px dashed var(--panel-border); padding-bottom: 0.25rem; display: inline-block;">HISTORIAL DE BITÁCORA</div>
                    <div style="max-height: 120px; overflow-y: auto; padding-right: 1rem; display: flex; flex-direction: column; gap: 0.5rem;">
                        ${init.logs.map(log => `
                            <div style="display: flex; gap: 1rem; align-items: baseline;">
                                <span style="font-size: 0.75rem; color: var(--primary); font-family: 'JetBrains Mono', monospace; white-space: nowrap;">[${log.date.split(' ')[0]}]</span>
                                <span style="font-size: 0.9rem; color: var(--text-main); font-family: 'Inter', sans-serif; line-height: 1.4;">${log.text}</span>
                            </div>
                        `).join('')}
                    </div>
                </td>
            </tr>` : ''}
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

window.switchTab = (tabName) => {
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
};


function renderClientsGrid() {
    const tbody = document.getElementById('clients-grid-body');
    tbody.innerHTML = '';
    
    const search = searchQuery.toLowerCase();
    const filtered = clientsData.filter(c => {
        return (c.name || '').toLowerCase().includes(search) || 
               (c.sponsor || '').toLowerCase().includes(search);
    });

    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No hay clientes</td></tr>';
        return;
    }

    filtered.forEach(clientData => {
        const count = initiatives.filter(i => i.client_id === clientData.id).length;
        
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.className = 'client-row';
        tr.onclick = (e) => {
            if (!e.target.closest('button') && !e.target.closest('a')) {
                editClient(clientData.id);
            }
        };
        tr.innerHTML = `
            <td>
                <strong>${clientData.name}</strong> ${getFlowsHtml(clientData.name)}
                <span class="tags-container">${(clientData.tags || []).map(t => `<span class="badge-tag ${t.toLowerCase()}">${t}</span>`).join('')}</span>
                ${clientData.attachments ? `<br><a href="${clientData.attachments}" target="_blank" style="font-size: 0.8rem; color: var(--info);">ðŸ“Ž Ver DocumentaciÃ³n</a>` : ''}
            </td>
            <td>${clientData.sponsor || '-'}</td>
            <td>
                <div>${formatNumber(clientData.volume)} OFs</div>
                <div style="font-size: 0.8rem; color: var(--text-muted)">${formatMoney(clientData.revenue)}</div>
            </td>
            <td><span class="badge" style="background: rgba(255,255,255,0.1)">${count} Pedida(s)</span></td>
            <td>
                <button class="btn-icon tooltip-container" style="margin-right: 0.5rem;" onclick="editClient('${clientData.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Editar Cliente</div>
                </button>
                <button class="btn-icon danger tooltip-container" onclick="deleteClientSoft('${clientData.id}')">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
                    <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Borrar Cliente (Oculta Pedidas)</div>
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

window.deleteClientSoft = async (id) => {
    if (!confirm('Â¿EstÃ¡s seguro de que quieres eliminar este cliente? Esto ocultarÃ¡ todas sus pedidas.')) return;
    try {
        const { error } = await client
            .from('clients')
            .update({ deleted_at: new Date().toISOString() })
            .eq('id', id);
        if (error) throw error;
        await fetchClients();
        await fetchInitiatives();
        if (document.getElementById('tab-clientes').classList.contains('active')) {
            renderClientsGrid();
        }
    } catch (err) {
        alert("Error al eliminar cliente: " + err.message);
    }
};

// History Logic
const historyGridBody = document.getElementById('history-grid-body');
const btnAddHistory = document.getElementById('btn-add-history');

function renderHistoryGrid() {
    historyGridBody.innerHTML = '';
    if (currentHistory.length === 0) {
        historyGridBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Sin historial</td></tr>';
        return;
    }
    currentHistory.forEach((item, index) => {
        const tr = document.createElement('tr');
        tr.style.cursor = 'pointer';
        tr.className = 'client-row';
        tr.onclick = (e) => {
            if (!e.target.closest('button') && !e.target.closest('a')) {
                editClient(clientData.id);
            }
        };
        tr.innerHTML = `
            <td>${item.month}</td>
            <td>${formatNumber(item.volume)}</td>
            <td>${formatMoney(item.revenue)}</td>
            <td><button type="button" onclick="removeHistoryItem(${index})" style="background: none; border: none; color: var(--danger); cursor: pointer;">X</button></td>
        `;
        historyGridBody.appendChild(tr);
    });
}

window.removeHistoryItem = (index) => {
    currentHistory.splice(index, 1);
    renderHistoryGrid();
};

btnAddHistory.addEventListener('click', () => {
    const month = document.getElementById('input-hist-month').value;
    const volume = document.getElementById('input-hist-volume').value;
    const revenue = document.getElementById('input-hist-revenue').value;
    
    if(!month) return alert('Debes seleccionar un mes');
    
    currentHistory.push({
        month,
        volume: parseInt(volume) || 0,
        revenue: parseInt(revenue) || 0
    });
    
    // Sort desc by month
    currentHistory.sort((a, b) => b.month.localeCompare(a.month));
    
    document.getElementById('input-hist-month').value = '';
    document.getElementById('input-hist-volume').value = '';
    document.getElementById('input-hist-revenue').value = '';
    renderHistoryGrid();
});

// Modal logic
let editingClientId = null;
let editingInitId = null;

function openClientModal(id = null) {
    editingClientId = id;
    if (id) {
        const client = clientsData.find(c => c.id === id);
        if(!client) return;
        document.getElementById('modal-client-title').textContent = 'Editar Cliente';
        document.getElementById('input-client-name').value = client.name || '';
        document.getElementById('input-client-sponsor').value = client.sponsor || '';
        document.getElementById('input-client-docs').value = client.general_documentation || '';
        document.getElementById('input-volume').value = client.volume || 0;
        document.getElementById('input-revenue').value = client.revenue || 0;
        
        const tags = client.tags || [];
        document.getElementById('tag-dispatch').checked = tags.includes('Dispatch');
        document.getElementById('tag-vtex').checked = tags.includes('VTEX');
        document.getElementById('tag-shopify').checked = tags.includes('Shopify');
        
        document.getElementById('input-client-file').value = '';
        document.getElementById('client-file-link').innerHTML = renderAttachments(client.attachments);
        currentHistory = Array.isArray(client.monthly_history) ? [...client.monthly_history] : [];
        renderHistoryGrid();
    } else {
        document.getElementById('modal-client-title').textContent = 'Nuevo Cliente';
        formClient.reset();
        document.getElementById('client-file-link').innerHTML = '';
        currentHistory = [];
        renderHistoryGrid();
    }
    modalClient.classList.add('active');
}

function openInitModal(id = null, preselectClientId = null) {
    editingInitId = id;
    if (id) {
        const init = initiatives.find(i => i.id === id);
        if(!init) return;
        document.getElementById('modal-init-title').textContent = 'Editar Iniciativa';
        document.getElementById('input-init-client-select').value = init.client_id || '';
        
        document.getElementById('input-name').value = init.name || '';
        document.getElementById('input-jira-url').value = init.jira_url || '';
        document.getElementById('input-documentation').value = init.documentation || '';
        document.getElementById('input-confluence-link').value = init.confluence_link || '';
          
        document.getElementById('input-init-file').value = '';
        document.getElementById('init-file-link').innerHTML = renderAttachments(init.attachments);
        document.getElementById('input-priority').value = init.priority || 0;
        document.getElementById('input-model').value = init.model || 'INHOUSE';
        document.getElementById('input-type').value = init.type || 'NATIVA_API';
        document.getElementById('input-complexity').value = init.complexity || 'MEDIA';
        document.getElementById('input-hh').value = init.hh || 0;
        document.getElementById('input-phase').value = init.phase || 'DISCOVERY';
        document.getElementById('input-owner').value = init.owner || 'TI';
        document.getElementById('input-bottleneck').value = init.bottleneck || '';
    } else {
        document.getElementById('modal-init-title').textContent = 'Nueva Iniciativa';
        formInit.reset();
        document.getElementById('init-file-link').innerHTML = '';
        document.getElementById('input-confluence-link').value = '';
          
        document.getElementById('input-init-client-select').value = preselectClientId || '';
        document.getElementById('input-priority').value = 0;
    }
    modalInit.classList.add('active');
}

window.editInitiative = openInitModal;
window.editClient = openClientModal;
window.openModalForClient = (clientId) => openInitModal(null, clientId);

function closeModals() {
    modalClient.classList.remove('active');
    modalInit.classList.remove('active');
    editingClientId = null;
    editingInitId = null;
}

// Event Listeners
formClient.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = formClient.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Guardando...';
    submitBtn.disabled = true;

    try {
        let newClientUrls = [];
        const files = document.getElementById('input-client-file').files;
        if (files && files.length > 0) {
            for(let f of files) {
                newClientUrls.push(await uploadFileToSupabase(f, 'attachments'));
            }
        }
        
        const tags = [];
        if (document.getElementById('tag-dispatch').checked) tags.push('Dispatch');
        if (document.getElementById('tag-vtex').checked) tags.push('VTEX');
        if (document.getElementById('tag-shopify').checked) tags.push('Shopify');
        
        const payload = {
            name: document.getElementById('input-client-name').value,
            sponsor: document.getElementById('input-client-sponsor').value,
            general_documentation: document.getElementById('input-client-docs').value,
            volume: parseInt(document.getElementById('input-volume').value) || 0,
            revenue: parseInt(document.getElementById('input-revenue').value) || 0,
            monthly_history: currentHistory,
            tags: tags
        };

        if (editingClientId) {
            const existingClient = clientsData.find(c => c.id === editingClientId);
            if (existingClient && existingClient.attachments) {
                try {
                    let oldFiles = JSON.parse(existingClient.attachments);
                    if (!Array.isArray(oldFiles)) oldFiles = [existingClient.attachments];
                    newClientUrls = [...oldFiles, ...newClientUrls];
                } catch(e) {
                    newClientUrls = [existingClient.attachments, ...newClientUrls];
                }
            }
        }

        if (newClientUrls.length > 0) {
            payload.attachments = JSON.stringify(newClientUrls);
        }

        let result;
        if (editingClientId) {
            result = await client.from('clients').update(payload).eq('id', editingClientId);
        } else {
            result = await client.from('clients').insert([payload]);
        }

        if (result.error) throw result.error;
        await fetchClients();
        if (document.getElementById('tab-clientes').classList.contains('active')) renderClientsGrid();
        renderGrid();
        closeModals();
    } catch (err) {
        alert("Error guardando cliente: " + err.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

formInit.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = formInit.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Guardando...';
    submitBtn.disabled = true;

    try {
        let newInitUrls = [];
        const files = document.getElementById('input-init-file').files;
        if (files && files.length > 0) {
            for(let f of files) {
                newInitUrls.push(await uploadFileToSupabase(f, 'attachments'));
            }
        }
        
        const payload = {
            client_id: document.getElementById('input-init-client-select').value,
            name: document.getElementById('input-name').value,
            jira_url: document.getElementById('input-jira-url').value,
            documentation: document.getElementById('input-documentation').value,
            confluence_link: document.getElementById('input-confluence-link').value,
              
            priority: parseInt(document.getElementById('input-priority').value) || 0,
            model: document.getElementById('input-model').value,
            type: document.getElementById('input-type').value,
            complexity: document.getElementById('input-complexity').value,
            hh: parseInt(document.getElementById('input-hh').value) || 0,
            phase: document.getElementById('input-phase').value,
            owner: document.getElementById('input-owner').value,
            estimated_date: document.getElementById('input-estimated-date').value,
            bottleneck: document.getElementById('input-bottleneck').value,
            updated_at: new Date().toISOString()
        };

        if (editingInitId) {
            const existingInit = initiatives.find(i => i.id === editingInitId);
            if (existingInit && existingInit.attachments) {
                try {
                    let oldFiles = JSON.parse(existingInit.attachments);
                    if (!Array.isArray(oldFiles)) oldFiles = [existingInit.attachments];
                    newInitUrls = [...oldFiles, ...newInitUrls];
                } catch(e) {
                    newInitUrls = [existingInit.attachments, ...newInitUrls];
                }
            }
        }

        if (newInitUrls.length > 0) {
            payload.attachments = JSON.stringify(newInitUrls);
        }

        let result;
        if (editingInitId) {
            result = await client.from('initiatives').update(payload).eq('id', editingInitId);
        } else {
            result = await client.from('initiatives').insert([payload]);
        }

        if (result.error) throw result.error;
        await fetchInitiatives();
        closeModals();
    } catch (err) {
        alert("Error guardando iniciativa: " + err.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

btnNewInit.addEventListener('click', () => openInitModal());
btnNewClient.addEventListener('click', () => openClientModal());
btnCloseClient.addEventListener('click', closeModals);
btnCloseInit.addEventListener('click', closeModals);
btnCancelClient.addEventListener('click', closeModals);
btnCancelInit.addEventListener('click', closeModals);
modalClient.addEventListener('click', (e) => { if (e.target === modalClient) closeModals(); });
modalInit.addEventListener('click', (e) => { if (e.target === modalInit) closeModals(); });

searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    if (document.getElementById('tab-clientes').classList.contains('active')) {
        renderClientsGrid();
    } else {
        renderGrid();
    }
});

// Init
fetchFlows().then(() => fetchClients()).then(() => fetchInitiatives());










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
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            text-decoration: none;
            color: var(--text-primary);
            transition: all 0.2s;
            cursor: pointer;
        `;
        card.onmouseover = () => { card.style.borderColor = 'var(--primary)'; card.style.transform = 'translateY(-2px)'; };
        card.onmouseout = () => { card.style.borderColor = 'var(--panel-border)'; card.style.transform = 'none'; };
        
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
        section.className = 'table-container';
        section.style.marginBottom = '2rem';
        
        // Header of the section
        const header = document.createElement('div');
        header.style.padding = '1rem 1.5rem';
        header.style.borderBottom = '1px solid var(--panel-border)';
        header.innerHTML = `<h3 style="margin:0;"><span class="badge-tag ${tag.toLowerCase()}">${tag}</span> <span style="font-size: 0.9rem; color: var(--text-muted); font-weight: normal;">(${clientsWithTag.length} Clientes)</span></h3>`;
        section.appendChild(header);
        
        // Table of clients
        const table = document.createElement('table');
        table.className = 'data-grid';
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
                    <tr style="cursor:pointer;" class="client-row" onclick="if(!event.target.closest('button') && !event.target.closest('a')) editClient('${c.id}');">
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


// Theme Toggle
window.toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    if (typeof renderCharts === 'function') renderCharts();
};

// Apply saved theme on load
const savedTheme = localStorage.getItem('theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);

// Initialize Log state
let currentLogs = [];

window.deleteLog = (index) => { currentLogs.splice(index, 1); renderLogs(); };

function renderLogs() {
    const container = document.getElementById('logs-container');
    if (!container) return;
    
    if (currentLogs.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem; text-align: center;">No hay registros en la bitácora.</p>';
        return;
    }
    
    container.innerHTML = currentLogs.map((log, index) => `
        <div class="log-entry" style="position: relative;">
            <button type="button" onclick="deleteLog(${index})" class="btn-icon" style="position: absolute; right: 0; top: 0.5rem; color: var(--danger); font-size: 1.1rem; border: none; background: transparent; cursor: pointer;">&times;</button>
            <div class="log-meta">${log.date} • ${log.author || 'Starken PMO'}</div>
            <div class="log-content">${log.text}</div>
        </div>
    `).join('');
}

const btnAddLog = document.getElementById('btn-add-log');
if(btnAddLog) {
    btnAddLog.addEventListener('click', () => {
        const input = document.getElementById('input-log-text');
        if (!input.value.trim()) return;
        
        const now = new Date();
        const dateStr = now.toISOString().split('T')[0] + ' ' + now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        currentLogs.unshift({
            date: dateStr,
            author: 'PMO (Cristóbal)',
            text: input.value.trim()
        });
        
        input.value = '';
        renderLogs();
    });
}

// Chart logic
let chartRevenueInstance = null;
let chartVolumeInstance = null;

function renderCharts() {
    try {
        const ctxRev = document.getElementById('chartRevenue');
        const ctxVol = document.getElementById('chartVolume');
        if (!ctxRev || !ctxVol) return;

        // Force parent heights
        ctxRev.parentElement.style.position = 'relative';
        ctxRev.parentElement.style.height = '400px';
        ctxVol.parentElement.style.position = 'relative';
        ctxVol.parentElement.style.height = '400px';

        const sortedByRevenue = [...clientsData].filter(c => c.revenue > 0).sort((a,b) => b.revenue - a.revenue);
        const sortedByVolume = [...clientsData].filter(c => c.volume > 0).sort((a,b) => b.volume - a.volume);

        if (!window.Chart) {
            ctxRev.parentElement.innerHTML += '<p style="color:red">Error: Chart.js no cargó.</p>';
            return;
        }

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
                    backgroundColor: 'rgba(29, 78, 216, 0.7)',
                    borderColor: 'rgba(29, 78, 216, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
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
                    backgroundColor: 'rgba(21, 128, 61, 0.7)',
                    borderColor: 'rgba(21, 128, 61, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { grid: { color: gridColor }, ticks: { callback: (val) => (val/1000).toFixed(0) + 'k' } },
                    x: { grid: { display: false } }
                },
                plugins: {
                    tooltip: { callbacks: { label: (ctx) => ' ' + ctx.raw.toLocaleString('es-CL') + ' OFs' } }
                }
            }
        });
    } catch (e) {
        document.getElementById('view-metricas').innerHTML += `<p style="color:red">Error JS: ${e.message}</p>`;
    }
}
