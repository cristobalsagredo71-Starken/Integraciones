import re
html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

toggle_html = '''
            <div style="display: flex; gap: 1rem; align-items: center; position: absolute; right: 2rem; top: 2rem;">
                <button id="theme-toggle" class="btn-icon tooltip-container" onclick="toggleTheme()" style="background: var(--panel-bg); border: 1px solid var(--panel-border); padding: 0.5rem; border-radius: 50%;">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                    <span class="tooltip-text" style="bottom:-30px;">Tema Claro/Oscuro</span>
                </button>
            </div>
'''

if 'id="theme-toggle"' not in html:
    html = re.sub(r'(<header class="header">)', r'\1\n' + toggle_html, html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Injected theme toggle.")
else:
    print("Theme toggle already exists.")
