try:
    import esprima
except ImportError:
    import os
    os.system("npm install -g esprima")
    
import subprocess
result = subprocess.run(["node", "-c", "app.js"], capture_output=True, text=True)
print("Node Output:", result.stderr)
