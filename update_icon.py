import re

content = open('app.js', 'r', encoding='utf-8').read()

# Replace getFlowsHtml to just return a tiny icon instead of a huge button
old_helper = r'return `<button class="badge-tag".*?🖥️ Flujos \(\$\{flows\.length\}\)</button>`;'
new_helper = """return `<span onclick="openFlowsModal('${clientName}')" class="tooltip-container" style="cursor:pointer; color: #10b981; font-size: 1.1rem; display: inline-flex; align-items: center; margin-left: 2px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 2px;"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
        <span style="font-size: 0.75rem; font-weight: bold;">${flows.length}</span>
        <div class="tooltip-text" style="bottom: 125%; left: 50%; transform: translateX(-50%); width: max-content; padding: 4px 8px;">Ver ${flows.length} Flujos</div>
    </span>`;"""

content = re.sub(old_helper, new_helper, content, flags=re.DOTALL)

open('app.js', 'w', encoding='utf-8').write(content)
print("Updated to use subtle icon")
