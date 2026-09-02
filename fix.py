import re

content = open('app.js', 'r', encoding='utf-8').read()

pattern = r'// Helper para renderizar multiples archivos.*?function renderAttachments.*?\} catch \(e\) \{.*?\}[\n\r\s]*\}'
replacement = '''// Helper para renderizar multiples archivos
function renderAttachments(attachmentsStr) {
    if (!attachmentsStr) return "";
    try {
        const arr = JSON.parse(attachmentsStr);
        if (Array.isArray(arr)) {
            return arr.map((url, i) => <a href="\" target="_blank" style="color: var(--info); font-size: 0.8rem; margin-right: 0.5rem; display: inline-block;">?? Archivo \</a>).join('');
        }
        return <a href="\" target="_blank" style="color: var(--info); font-size: 0.8rem;">?? Archivo</a>;
    } catch (e) {
        return <a href="\" target="_blank" style="color: var(--info); font-size: 0.8rem;">?? Archivo</a>;
    }
}
'''
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
open('app.js', 'w', encoding='utf-8').write(new_content)
print('Fixed renderAttachments')
