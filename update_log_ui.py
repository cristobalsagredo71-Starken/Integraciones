import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update renderLogs
old_renderLogs = """    container.innerHTML = currentLogs.map(log => `
        <div class="log-entry">
            <div class="log-meta">${log.date} • ${log.author || 'Starken PMO'}</div>
            <div class="log-content">${log.text}</div>
        </div>
    `).join('');"""

new_renderLogs = """    container.innerHTML = currentLogs.map((log, index) => `
        <div class="log-entry" style="position: relative;">
            <button type="button" onclick="deleteLog(${index})" class="btn-icon" style="position: absolute; right: 0; top: 0.5rem; color: var(--danger); font-size: 1.1rem; border: none; background: transparent; cursor: pointer;">&times;</button>
            <div class="log-meta">${log.date} • ${log.author || 'Starken PMO'}</div>
            <div class="log-content">${log.text}</div>
        </div>
    `).join('');"""

js = js.replace(old_renderLogs, new_renderLogs)

if "window.deleteLog" not in js:
    js = js.replace("function renderLogs() {", "window.deleteLog = (index) => { currentLogs.splice(index, 1); renderLogs(); };\n\nfunction renderLogs() {")

# 2. Update renderInitRow table view
old_nested = """${(init.logs && init.logs.length > 0) ? `
            <tr style="background: rgba(0,0,0,0.02);">
                <td colspan="8" style="padding: 0.5rem 1rem 1rem 3rem; border-bottom: 1px solid var(--panel-border);">
                    <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                        <span style="font-size: 0.75rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">ÚLTIMO HITO REGISTRADO (${init.logs[0].date.split(' ')[0]})</span>
                        <span style="font-size: 0.9rem; color: var(--text-main); font-family: 'Inter', sans-serif;">${init.logs[0].text}</span>
                    </div>
                </td>
            </tr>` : ''}"""

new_nested = """${(init.logs && init.logs.length > 0) ? `
            <tr style="background: var(--bg-color);">
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
            </tr>` : ''}"""

js = js.replace(old_nested, new_nested)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS successfully")
