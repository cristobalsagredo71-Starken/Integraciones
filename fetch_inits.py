import json
import urllib.request
url = "https://dzmsfxnvfardckddvzjt.supabase.co/rest/v1/initiatives?select=*"
req = urllib.request.Request(url, headers={
    "apikey": "sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN",
    "Authorization": "Bearer sb_publishable_J0eJ5rRXzERV8RxiYk95sg_NTd8JWYN"
})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        if data:
            print(data[0])
except Exception as e:
    print(e)
