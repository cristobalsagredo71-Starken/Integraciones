import re
content = open('app.js', 'r', encoding='utf-8').read()

old_confluence = r'rgba\(23, 43, 77, 0\.2\); color: #172b4d; border: 1px solid rgba\(23,43,77,0\.4\)'
new_confluence = r'rgba(0, 184, 217, 0.2); color: #00b8d9; border: 1px solid rgba(0, 184, 217, 0.4)'

content = re.sub(old_confluence, new_confluence, content)

open('app.js', 'w', encoding='utf-8').write(content)
print("Done fixing Confluence color")
