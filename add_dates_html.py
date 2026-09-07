with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_fields = """
                        <div class="form-group" style="margin-top: 1rem;">
                            <label style="color: var(--primary);">Fechas Discovery</label>
                            <div style="display: flex; gap: 1rem;">
                                <div style="flex: 1;">
                                    <label style="font-size: 0.8rem;">Inicio</label>
                                    <input type="date" id="input-date-start-discovery">
                                </div>
                                <div style="flex: 1;">
                                    <label style="font-size: 0.8rem;">Fin</label>
                                    <input type="date" id="input-date-end-discovery">
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <label style="color: var(--primary);">Fechas Diseño</label>
                            <div style="display: flex; gap: 1rem;">
                                <div style="flex: 1;">
                                    <label style="font-size: 0.8rem;">Inicio</label>
                                    <input type="date" id="input-date-start-design">
                                </div>
                                <div style="flex: 1;">
                                    <label style="font-size: 0.8rem;">Fin</label>
                                    <input type="date" id="input-date-end-design">
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <label style="color: var(--primary);">Fechas Desarrollo</label>
                            <div style="display: flex; gap: 1rem;">
                                <div style="flex: 1;">
                                    <label style="font-size: 0.8rem;">Inicio</label>
                                    <input type="date" id="input-date-start-dev">
                                </div>
                                <div style="flex: 1;">
                                    <label style="font-size: 0.8rem;">Fin</label>
                                    <input type="date" id="input-date-end-dev">
                                </div>
                            </div>
                        </div>
"""
import re
html = re.sub(r'(<input type="date" id="input-estimated-date">\s*</div>)', r'\1' + new_fields, html, flags=re.DOTALL)

with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "w", encoding="utf-8") as f:
    f.write(html)
