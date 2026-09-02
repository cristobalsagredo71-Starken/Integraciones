import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

theme_code = """
// Theme Toggle
window.toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
};

// Apply saved theme on load
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);

// Initialize Log state
let currentLogs = [];

function renderLogs() {
    const container = document.getElementById('logs-container');
    if (!container) return;
    
    if (currentLogs.length === 0) {
        container.innerHTML = '<p style="color: var(--text-muted); font-size: 0.85rem; text-align: center;">No hay registros en la bitácora.</p>';
        return;
    }
    
    container.innerHTML = currentLogs.map(log => `
        <div class="log-entry">
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
"""

# Append to the end of app.js
if "window.toggleTheme" not in js:
    js += "\n" + theme_code

# Update openInitModal to populate logs
init_modal_target = r"document\.getElementById\('input-actual-end'\)\.value\s*=\s*init\.actual_end_date\s*\|\|\s*'';"
init_modal_replacement = r"document.getElementById('input-actual-end').value = init.actual_end_date || '';\n        currentLogs = Array.isArray(init.logs) ? [...init.logs] : [];\n        renderLogs();"
js = re.sub(init_modal_target, init_modal_replacement, js)

# Update new init creation (else block)
new_init_target = r"document\.getElementById\('input-actual-end'\)\.value\s*=\s*'';"
new_init_replacement = r"document.getElementById('input-actual-end').value = '';\n        currentLogs = [];\n        renderLogs();"
js = re.sub(new_init_target, new_init_replacement, js)

# Update formInit submit to include logs
submit_target = r"actual_end_date:\s*document\.getElementById\('input-actual-end'\)\.value\s*\|\|\s*null"
submit_replacement = r"actual_end_date: document.getElementById('input-actual-end').value || null,\n        logs: currentLogs"
js = re.sub(submit_target, submit_replacement, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated app.js")
