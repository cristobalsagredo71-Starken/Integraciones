content = open('app.js', 'r', encoding='utf-8').read()
content = content.replace('class="btn-close-modal"', 'class="close-btn"')
open('app.js', 'w', encoding='utf-8').write(content)
print("Fixed close button")
