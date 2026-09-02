import re

js_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js"
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# We need to find the return statement of renderInitRow and inject our nested TR for the last log.
# Since python string replacement is easier if we just match the end of the TR.
# renderInitRow returns a string like: return ` <tr> ... </tr> `;

target = """</button>
                </td>
            </tr>"""

replacement = """</button>
                </td>
            </tr>
            ${(init.logs && init.logs.length > 0) ? `
            <tr style="background: rgba(0,0,0,0.02);">
                <td colspan="8" style="padding: 0.5rem 1rem 1rem 3rem; border-bottom: 1px solid var(--panel-border);">
                    <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                        <span style="font-size: 0.75rem; color: var(--text-muted); font-family: 'JetBrains Mono', monospace;">ÚLTIMO HITO REGISTRADO (${init.logs[0].date.split(' ')[0]})</span>
                        <span style="font-size: 0.9rem; color: var(--text-main); font-family: 'Inter', sans-serif;">${init.logs[0].text}</span>
                    </div>
                </td>
            </tr>` : ''}"""

js = js.replace(target, replacement)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS")
