import json
import urllib.request

url = "https://dzmsfxnvfardckddvzjt.supabase.co/rest/v1/initiatives?select=id,name,client_id,phase"
req = urllib.request.Request(url, headers={
    "apikey": "sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN",
    "Authorization": "Bearer sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN"
})

try:
    with urllib.request.urlopen(req) as response:
        inits = json.loads(response.read().decode())
        print("Initiatives found:")
        for i in inits:
            print(f"- {i['name']} (Phase: {i['phase']}, ClientID: {i['client_id']})")
except Exception as e:
    print(e)
