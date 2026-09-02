import re

content = open('app.js', 'r', encoding='utf-8').read()

# Remove getFlowsHtml from client name in renderGrid
target1 = r'\s*\$\{getFlowsHtml\(client\.name\)\}'
content = re.sub(target1, '', content)

# Inject getFlowsHtml into initiative name in renderGrid
target2 = r'(<strong style="font-size: 1\.05rem;">\$\{init\.name\}</strong>)'
replacement2 = r'\1 ${getFlowsHtml(init.name)}'
content = re.sub(target2, replacement2, content)

# Make sure openFlowsModal takes initiative name and formats the modal title properly
# We just need to change the CSS of the button slightly to align it with the initiative name
target3 = r'style="cursor:pointer; color: #10b981; font-size: 1\.1rem; display: inline-flex; align-items: center; margin-left: 2px;"'
replacement3 = r'style="cursor:pointer; color: #10b981; font-size: 1.1rem; display: inline-flex; align-items: center; margin-left: 8px; vertical-align: middle;"'
content = content.replace(target3, replacement3)

open('app.js', 'w', encoding='utf-8').write(content)
print("Updated JS to map by Initiative Name")
