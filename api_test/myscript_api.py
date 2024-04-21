import hmac
import hashlib
import binascii
import json
import requests

def compute_hmac(application_key, hmac_key, json_input):
    user_key = application_key + hmac_key
    user_key = bytes(user_key, 'utf-8')
    json_input = bytes(json.dumps(json_input), 'utf-8')

    signature = hmac.new(user_key, json_input, digestmod=hashlib.sha512).digest()
    return binascii.hexlify(signature).decode()

application_key = "6aa542de-0173-457d-9069-c5cf70b9676e"
hmac_key = "b9eb26bf-99f9-415b-8f88-3aaf55c5951f"
with open("coordinates_myscript.json", "r", encoding="utf-8") as file:
    json_input = json.loads(file.read())
signature = compute_hmac(application_key, hmac_key, json_input)
print(signature)  # 输出签名

# send request
# target request:
"""
curl -X 'POST' \
  'https://cloud.myscript.com/api/v4.0/iink/batch' \
  -H 'accept: */*' \
  -H 'applicationKey: 6aa542de-0173-457d-9069-c5cf70b9676e' \
  -H 'myscript-client-name: qwer' \
  -H 'myscript-client-version: asdf' \
  -H 'hmac: b9eb26bf-99f9-415b-8f88-3aaf55c5951f' \
  -H 'Content-Type: application/json' \
  -d '{ ... json_input ... }'
"""

headers_myscript = {
    "Accept": "text/plain, application/x-latex",
    "applicationKey": application_key,
    "myscript-client-name": "qwer",
    "myscript-client-version": "asdf",
    "hmac": signature,
    "Content-Type": "application/json",
}
r = requests.post(
    "https://cloud.myscript.com/api/v4.0/iink/batch",
    json=json_input,
    headers=headers_myscript,
)
print(r.status_code)
print(r.text)
# print(json.dumps(r.json(), indent=4, sort_keys=True, ensure_ascii=False))