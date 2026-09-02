import os

files = ['index.html', 'app.js']
replacements = {
    'Dueo (Baln)': 'Responsable',
    'Dueo del Baln': 'Responsable',
    'Integracin': 'Integración',
    'Configuracin': 'Configuración',
    'Facturacin': 'Facturación',
    'Tcnico': 'Técnico',
    'tcnico': 'técnico',
    'Tcnica': 'Técnica',
    'tcnica': 'técnica',
    'Especfica': 'Específica',
    'Documentacin': 'Documentación',
    'bsqueda': 'búsqueda',
    'Aadir': 'Añadir',
    'Conexin': 'Conexión',
    'Asegrate': 'Asegúrate',
    'Aseg\u01e7rate': 'Asegúrate',
    'Asegǧrate': 'Asegúrate',
    'b\u01e7squeda': 'búsqueda',
    'bǧsqueda': 'búsqueda',
    'Y"Z': '📎',
    's?': '🛑',
    '-': '↗'
}

for file in files:
    try:
        # Intenta leer asumiendo UTF-8 (aunque tenga errores)
        content = open(file, 'r', encoding='utf-8', errors='replace').read()
        
        for k, v in replacements.items():
            content = content.replace(k, v)
        
        open(file, 'w', encoding='utf-8').write(content)
        print(f"Fixed {file}")
    except Exception as e:
        print(f"Error {file}: {e}")
