content = open('index.html', 'r', encoding='utf-8').read()
content = content.replace('\u2197', '-')
open('index.html', 'w', encoding='utf-8').write(content)

content_js = open('app.js', 'r', encoding='utf-8').read()
content_js = content_js.replace('\u2197', '-')
open('app.js', 'w', encoding='utf-8').write(content_js)
print("Restored hyphens")
