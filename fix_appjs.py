content = open('app.js', 'r', encoding='utf-8').read()

# Fix client stop sign
content = content.replace('init.client🛑', 'init.clients?')

# Fix weird encoding in priority badge
content = content.replace("' Y\"' : ''", "' 🔥' : ''")

# Replace any other weird characters introduced by encoding fail
content = content.replace('CONFIGURACI\xc3\u201cN', 'CONFIGURACIÓN')
content = content.replace('\xc3\u201c', 'Ó')
content = content.replace('\xc3\x81', 'Á')
content = content.replace('\xc3\x89', 'É')
content = content.replace('\xc3\x8d', 'Í')
content = content.replace('\xc3\x9a', 'Ú')
content = content.replace('\xc3\xb1', 'ñ')

open('app.js', 'w', encoding='utf-8').write(content)
print("Done fixing app.js")
