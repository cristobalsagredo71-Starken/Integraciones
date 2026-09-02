with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
match = re.search(r'(<div class="toolbar">.*?</button>\s*</div>\s*</div>)(.*?)(<div id="view-conductor")', html, re.DOTALL)
if match:
    print("Found toolbar and whatever is after it:")
    print(match.group(2)[:500]) # Print first 500 chars after toolbar
else:
    print("Could not find toolbar layout")
