with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "r", encoding="utf-8") as f:
    js = f.read()

import re
# The correct function ends at:
#     } catch (e) {
#         document.getElementById('view-metricas').innerHTML += `<p style="color:red">Error JS: ${e.message}</p>`;
#     }
# }
# Everything after that in the file is garbage.

good_part = js[:js.find('    const sortedByRevenue = [...clients].filter(c => c.revenue > 0)')]

# Actually, let's be more precise.
# Find the exact string of the new renderCharts closing bracket
end_marker = "    }\n}"
end_pos = js.rfind(end_marker)
if end_pos != -1:
    # but wait, maybe there is another "    }\n}"?
    pass

# The garbage starts exactly at:
garbage_start = js.find("    const sortedByRevenue = [...clients].filter(c => c.revenue > 0)", js.find("Error JS:"))
if garbage_start != -1:
    clean_js = js[:garbage_start].strip() + "\n"
    with open(r"C:\Users\cristobal.sagredo\Desktop\Obsidian\10 Proyectos\maestro-integraciones\app.js", "w", encoding="utf-8") as f:
        f.write(clean_js)
    print("Fixed syntax error")
else:
    print("Could not find garbage start")
