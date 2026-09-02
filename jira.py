import re

content = open('app.js', 'r', encoding='utf-8').read()

content = re.sub(r'documentation: document\.getElementById\(\'input-documentation\'\)\.value,', r'documentation: document.getElementById(\'input-documentation\').value,\n            jira_link: document.getElementById(\'input-jira-link\').value,', content)

content = re.sub(r'document\.getElementById\(\'input-documentation\'\)\.value = init\.documentation \|\| \'\';', r'document.getElementById(\'input-documentation\').value = init.documentation || \'\';\n        document.getElementById(\'input-jira-link\').value = init.jira_link || \'\';', content)

content = re.sub(r'document\.getElementById\(\'init-file-link\'\)\.innerHTML = \'\';', r'document.getElementById(\'init-file-link\').innerHTML = \'\';\n        document.getElementById(\'input-jira-link\').value = \'\';', content)

badge_html = r"""<strong>${item.name}</strong>
                  ${item.jira_link ? `<a href="${item.jira_link}" target="_blank" class="badge-tag" style="background: rgba(38, 132, 255, 0.2); color: #4c9aff; border: 1px solid rgba(38,132,255,0.4); text-decoration: none; margin-left: 5px;">Jira ↗</a>` : ''}"""
content = content.replace('<strong>${item.name}</strong>', badge_html)

open('app.js', 'w', encoding='utf-8').write(content)
print('Done Jira JS update')
