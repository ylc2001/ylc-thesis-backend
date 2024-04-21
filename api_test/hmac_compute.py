import hmac
import hashlib
import binascii
import json

def compute_hmac(application_key, hmac_key, json_input):
    user_key = application_key + hmac_key
    user_key = bytes(user_key, 'utf-8')
    json_input = bytes(json.dumps(json_input), 'utf-8')

    signature = hmac.new(user_key, json_input, digestmod=hashlib.sha512).digest()
    return binascii.hexlify(signature).decode()

application_key = "6aa542de-0173-457d-9069-c5cf70b9676e"
hmac_key = "b9eb26bf-99f9-415b-8f88-3aaf55c5951f"

# 这里打开的 example_request.json 就是网页中给出的示例 request body.
with open("example_request.json", "r", encoding="utf-8") as file:
    json_input = json.loads(file.read())
signature = compute_hmac(application_key, hmac_key, json_input)
print(signature)  # 输出签名