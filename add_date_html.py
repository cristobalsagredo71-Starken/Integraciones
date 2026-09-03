with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_field = """
                        <div class="form-group">
                            <label>Fecha Estimada (Go Live)</label>
                            <input type="date" id="input-estimated-date">
                        </div>
"""
import re
# Insert after input-owner
html = re.sub(r'(<select id="input-owner">.*?</select>\s*</div>)', r'\1' + new_field, html, flags=re.DOTALL)

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "w", encoding="utf-8") as f:
    f.write(html)
