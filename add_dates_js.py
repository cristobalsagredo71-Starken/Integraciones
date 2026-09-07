with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re

# Payload injection
payload_fields = """            estimated_date: document.getElementById('input-estimated-date').value,
            date_start_discovery: document.getElementById('input-date-start-discovery').value,
            date_end_discovery: document.getElementById('input-date-end-discovery').value,
            date_start_design: document.getElementById('input-date-start-design').value,
            date_end_design: document.getElementById('input-date-end-design').value,
            date_start_dev: document.getElementById('input-date-start-dev').value,
            date_end_dev: document.getElementById('input-date-end-dev').value,"""
js = re.sub(r'estimated_date: document\.getElementById\(\'input-estimated-date\'\)\.value,', payload_fields, js)

# Populate form
populate_fields = """    document.getElementById('input-estimated-date').value = init.estimated_date || '';
    document.getElementById('input-date-start-discovery').value = init.date_start_discovery || '';
    document.getElementById('input-date-end-discovery').value = init.date_end_discovery || '';
    document.getElementById('input-date-start-design').value = init.date_start_design || '';
    document.getElementById('input-date-end-design').value = init.date_end_design || '';
    document.getElementById('input-date-start-dev').value = init.date_start_dev || '';
    document.getElementById('input-date-end-dev').value = init.date_end_dev || '';"""
js = re.sub(r'document\.getElementById\(\'input-estimated-date\'\)\.value = init\.estimated_date \|\| \'\';', populate_fields, js)

# Reset form
reset_fields = """    document.getElementById('input-estimated-date').value = '';
    document.getElementById('input-date-start-discovery').value = '';
    document.getElementById('input-date-end-discovery').value = '';
    document.getElementById('input-date-start-design').value = '';
    document.getElementById('input-date-end-design').value = '';
    document.getElementById('input-date-start-dev').value = '';
    document.getElementById('input-date-end-dev').value = '';"""
js = re.sub(r'document\.getElementById\(\'input-estimated-date\'\)\.value = \'\';', reset_fields, js)

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "w", encoding="utf-8") as f:
    f.write(js)
