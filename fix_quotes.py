import re
content = open('app.js', 'r', encoding='utf-8').read()
content = content.replace(r"\'", "'")
open('app.js', 'w', encoding='utf-8').write(content)
