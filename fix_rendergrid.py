import re

content = open('app.js', 'r', encoding='utf-8').read()

target = r'<div style="font-size: 0\.8rem; color: var\(--text-muted\); margin-bottom: 0\.2rem;">\s*\$\{client\.name \|\| \'Sin Cliente\'\}\s*\$\{\(client\.tags \|\| \[\]\)\.map\(t => `<span class="badge-tag \$\{t\.toLowerCase\(\)\}" style="transform: scale\(0\.8\); display: inline-block;">\$\{t\}</span>`\)\.join\(\'\'\)\}\s*</div>'

replacement = """<div style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.2rem; display: flex; align-items: center; gap: 8px;">
                      <span>${client.name || 'Sin Cliente'} ${(client.tags || []).map(t => `<span class="badge-tag ${t.toLowerCase()}" style="transform: scale(0.8); display: inline-block;">${t}</span>`).join('')}</span>
                      ${getFlowsHtml(client.name)}
                  </div>"""

content = re.sub(target, replacement, content)

open('app.js', 'w', encoding='utf-8').write(content)
print("Fixed renderGrid replacement")
