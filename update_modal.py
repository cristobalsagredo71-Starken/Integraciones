import re

content = open('app.js', 'r', encoding='utf-8').read()

# Replace the helper function
old_helper = r'function getFlowsHtml\(clientName\) \{.*?</details>`;\s*\}'

new_helper = """
function getFlowsHtml(clientName) {
    const flows = clientFlows[clientName];
    if (!flows || flows.length === 0) return '';
    
    return `<button class="badge-tag" onclick="openFlowsModal('${clientName}')" style="cursor:pointer; background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4); margin-top: 2px;">🖥️ Flujos (${flows.length})</button>`;
}

function openFlowsModal(clientName) {
    const flows = clientFlows[clientName];
    if (!flows || flows.length === 0) return;
    
    // Remove existing modal if any
    const existing = document.getElementById('dynamic-flows-modal');
    if (existing) existing.remove();
    
    let linksHtml = flows.map(f => `<a href="${f.url}" target="_blank" class="badge-tag" style="display: block; padding: 12px; margin-bottom: 8px; background: rgba(255,255,255,0.05); color: var(--text-primary); text-decoration: none; border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; font-size: 0.9rem; text-align: center;">📄 ${f.name}</a>`).join('');
    
    const modalHtml = `
    <div id="dynamic-flows-modal" class="modal active" style="z-index: 9999;">
        <div class="modal-content" style="max-width: 400px; text-align: center;">
            <div class="modal-header">
                <h2>Flujos: ${clientName}</h2>
                <button class="btn-close-modal" onclick="document.getElementById('dynamic-flows-modal').remove()">&times;</button>
            </div>
            <div style="padding: 20px 0;">
                ${linksHtml}
            </div>
        </div>
    </div>`;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}
"""

content = re.sub(old_helper, new_helper, content, flags=re.DOTALL)

open('app.js', 'w', encoding='utf-8').write(content)
print("Updated to use a sleek Modal instead of details tag")
