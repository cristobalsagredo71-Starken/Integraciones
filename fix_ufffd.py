import os

files = ['index.html', 'app.js']

for file in files:
    content = open(file, 'r', encoding='utf-8').read()
    
    # Check if there are any replacement chars
    count = content.count('\ufffd')
    if count > 0:
        print(f"Found {count} replacement chars in {file}")
        # Manually fixing the common ones based on context
        content = content.replace('Due\ufffdo (Bal\ufffdn)', 'Responsable')
        content = content.replace('Due\ufffdo del Bal\ufffdn', 'Responsable')
        content = content.replace('Documentaci\ufffdn', 'Documentación')
        content = content.replace('Espec\ufffdfica', 'Específica')
        content = content.replace('T\ufffdcnico', 'Técnico')
        content = content.replace('t\ufffdcnico', 'técnico')
        content = content.replace('Integraci\ufffdn', 'Integración')
        content = content.replace('b\ufffdsqueda', 'búsqueda')
        content = content.replace('\ufffdY"Z', '📎')
        content = content.replace('\ufffds\ufffd?', '🛑')
        content = content.replace('A\ufffdadir', 'Añadir')
        content = content.replace('Conexi\ufffdn', 'Conexión')
        content = content.replace('Aseg\ufffdrate', 'Asegúrate')
        content = content.replace('-\ufffd', '↗')
        content = content.replace('Jira \ufffd-', 'Jira ↗')
        content = content.replace('Confluence \ufffd-', 'Confluence ↗')
        
        open(file, 'w', encoding='utf-8').write(content)
        print(f"Fixed {file}")
