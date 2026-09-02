html_path = r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if '<div class="header">' in line:
        new_lines.append('''        <div style="display: flex; gap: 1rem; align-items: center; position: absolute; right: 2rem; top: 2.5rem;">
            <button id="theme-toggle" class="btn-icon tooltip-container" onclick="toggleTheme()" style="background: var(--panel-bg); border: 1px solid var(--panel-border);">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                <span class="tooltip-text" style="bottom:-30px;">Tema Claro/Oscuro</span>
            </button>
        </div>\n''')

with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Theme toggle injected")
