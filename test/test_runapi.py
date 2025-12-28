import http.client
import json

API_BASE_URL = "https://runapi.co"
API_HOST = "runapi.co"

conn = http.client.HTTPSConnection(API_HOST)
payload = json.dumps({
   "model": "gpt-5.1",
   "messages": [
      {
         "role": "user",
         "content": "你好呀?"
      }
   ]
})
headers = {
   'Accept': 'application/json',
   'Authorization': 'Bearer sk-HT0qrPan7RvyKaE1blXyjHHRABa1yhfxozJTt8RC4sTJ2SG7',
   'Content-Type': 'application/json'
}
conn.request("POST", "/v1/chat/completions", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))