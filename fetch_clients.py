import json
import urllib.request

url = "https://dzmsfxnvfardckddvzjt.supabase.co/rest/v1/clients?select=*"
req = urllib.request.Request(url, headers={
    "apikey": "sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN",
    "Authorization": "Bearer sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN"
})

try:
    with urllib.request.urlopen(req) as response:
        clients = json.loads(response.read().decode())
        print("Number of clients:", len(clients))
        if clients:
            c = clients[0]
            print("Fields:", list(c.keys()))
            print("Sample Client:", c['name'])
            print("Sample monthly_history:", c.get('monthly_history'))
            
            # Show all client names
            print("\nAll clients:", [cl['name'] for cl in clients])
except Exception as e:
    print("Error:", e)
