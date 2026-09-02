import re

# Update HTML
html = open('index.html', 'r', encoding='latin-1').read()
html = html.replace('<label>Link del ticket en Jira</label>', '<label>Link a Ticket de Jira (Opcional)</label>')
html = html.replace('<label>Link a Ticket de Jira (Opcional)</label>\n                            <input type="url" id="input-jira-link" placeholder="Ej: https://jira.starken.cl/browse/PRY-123">', '<label>Link de Confluence (Opcional)</label>\n                            <input type="url" id="input-confluence-link" placeholder="Ej: https://starken.atlassian.net/wiki/spaces/...">')
html = html.replace('<label>Link a Ticket de Jira (Opcional)</label>\n                              <input type="url" id="input-jira-link" placeholder="Ej: https://jira.starken.cl/browse/PRY-123">', '<label>Link de Confluence (Opcional)</label>\n                              <input type="url" id="input-confluence-link" placeholder="Ej: https://starken.atlassian.net/wiki/spaces/...">')
open('index.html', 'w', encoding='latin-1').write(html)

# Update JS
js = open('app.js', 'r', encoding='utf-8', errors='replace').read()
js = js.replace("document.getElementById('input-jira-link').value = init.jira_link || '';", "document.getElementById('input-confluence-link').value = init.confluence_link || '';")
js = js.replace("jira_link: document.getElementById('input-jira-link').value,", "confluence_link: document.getElementById('input-confluence-link').value,")
js = js.replace("document.getElementById('input-jira-link').value = '';", "document.getElementById('input-confluence-link').value = '';")

badge_html = r"""<strong style="font-size: 1.05rem;">${init.name}</strong>
                ${init.jira_url ? `<a href="${init.jira_url}" target="_blank" class="badge-tag" style="background: rgba(38, 132, 255, 0.2); color: #4c9aff; border: 1px solid rgba(38,132,255,0.4); text-decoration: none; margin-left: 5px;">Jira ↗</a>` : ''}
                ${init.confluence_link ? `<a href="${init.confluence_link}" target="_blank" class="badge-tag" style="background: rgba(23, 43, 77, 0.2); color: #172b4d; border: 1px solid rgba(23,43,77,0.4); text-decoration: none; margin-left: 5px;">Confluence ↗</a>` : ''}"""
js = re.sub(r'<strong style="font-size: 1\.05rem;">\$\{init\.name\}</strong>\s*\$\{init\.jira_link \? `<a href="\$\{init\.jira_link\}"[^>]+>.*?</a>` : \'\'\}', badge_html, js, flags=re.DOTALL)

open('app.js', 'w', encoding='utf-8').write(js)
print('Done!')
