import re

# Remove from HTML
html = open('index.html', 'r', encoding='utf-8').read()
html = re.sub(r'<div class="form-group full-width">\s*<label>Link a Flujo HTML \(Opcional\)</label>\s*<input type="text" id="input-flow-link"[^>]+>\s*</div>', '', html)
open('index.html', 'w', encoding='utf-8').write(html)

# Remove from JS (the form logic and grid logic)
js = open('app.js', 'r', encoding='utf-8').read()
js = re.sub(r'flow_url:\s*document\.getElementById\(\'input-flow-link\'\)\.value,', '', js)
js = re.sub(r'document\.getElementById\(\'input-flow-link\'\)\.value\s*=\s*init\.flow_url\s*\|\|\s*\'\';', '', js)
js = re.sub(r'document\.getElementById\(\'input-flow-link\'\)\.value\s*=\s*\'\';', '', js)
# Remove the old inline badge from the initiative name
js = re.sub(r'\$\{init\.flow_url \? `<a href="\$\{init\.flow_url\}" target="_blank"[^>]+>.*?</a>` : \'\'\}', '', js)

open('app.js', 'w', encoding='utf-8').write(js)
print("Cleaned up manual form fields")
