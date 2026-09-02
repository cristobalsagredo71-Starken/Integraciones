content = open('app.js', 'r', encoding='utf-8').read()

# Fix the modal class
content = content.replace('class="modal active"', 'class="modal-overlay active"')

open('app.js', 'w', encoding='utf-8').write(content)
print("Fixed modal class")
