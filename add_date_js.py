with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
# Add to payload
js = re.sub(r'(owner: document\.getElementById\(\'input-owner\'\)\.value,)', r"\1\n            estimated_date: document.getElementById('input-estimated-date').value,", js)

# Add to form population
js = re.sub(r"(document\.getElementById\(\'input-owner\'\)\.value = init\.owner \|\| \'POR DEFINIR\';)", r"\1\n    document.getElementById('input-estimated-date').value = init.estimated_date || '';", js)

# Add to form reset
js = re.sub(r"(document\.getElementById\(\'input-owner\'\)\.value = \'POR DEFINIR\';)", r"\1\n    document.getElementById('input-estimated-date').value = '';", js)

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "w", encoding="utf-8") as f:
    f.write(js)
