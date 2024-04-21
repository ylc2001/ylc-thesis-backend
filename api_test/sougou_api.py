import requests
import json
import time
import hashlib
import hmac
import base64
import os

file_name = "write10_sougou.json"

secretId = "2dfRj3hqmgmQCUnQjLv1v7Z4qre"
secretKey = "uVB6Z43NxF9acLVtMtU2FGbvWkBuOsRUSimLBzlzWi0="

# get current timestamp
current_timestamp = str(int(time.time()))

nonce = "67979"

file_path = os.path.join(os.getcwd(), "test_data", file_name)
print(file_path)

with open(file_path, "r", encoding="utf-8") as file:
    json_input = json.loads(file.read())

hash_object = hashlib.sha256()
hash_object.update(json.dumps(json_input).encode())
content_hash = hash_object.hexdigest()
print(f"content_hash: {content_hash}")

signature_gen = f"POSThttps://openapi.shurufa.sogou.com/track/v1/recognize?Action=TrackRecognize&Content-Hash={content_hash}&Nonce={nonce}&SecretId={secretId}&Service=Handwriting&Timestamp={current_timestamp}"

# 首先使用 HMAC-SHA256 算法对上一步中获得的签名原文字符串进行签名，然后将生成的签名串使用 Base64 进行编码，即可获得最终的签名串。

signature = hmac.new(secretKey.encode(), signature_gen.encode(), hashlib.sha256).digest()
signature = base64.b64encode(signature)
print(f"signature: {signature}")

headers_sougou = {
    'X-TC-Service': 'Handwriting',
    'Content-Type': 'application/json',
    'X-TC-Action': 'TrackRecognize',
    'X-TC-SecretId': secretId,
    'X-TC-Timestamp': current_timestamp,
    'X-TC-Nonce': nonce,
    'X-TC-Signature': signature
}

r = requests.post(
    "https://openapi.shurufa.sogou.com/track/v1/recognize",
    json=json_input,
    headers=headers_sougou,
)
print(r.status_code)
print(r.text)
print(json.dumps(r.json(), indent=4, sort_keys=True, ensure_ascii=False))