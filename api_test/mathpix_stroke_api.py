import requests
import json
import os

file_name = "long1_mathpix.json"

headers_mathpix = {
    "app_id": "tsinghuapcg_949548_75f42d",  # 替换为你的app_id
    "app_key": "0b5ad885c2ac8a7387ee62cf5f6bbf69e0494e1dc93257cc4fe581addc4d45f1",  # 替换为你的app_key
    "Content-type": "application/json",
}

# find the file in ./test_data/

file_path = os.path.join(os.getcwd(), "test_data", file_name)
print(file_path)

# put input strokes here
with open(file_path, "r", encoding="utf-8") as file:
    strokes = json.loads(file.read())
r = requests.post(
    "https://api.mathpix.com/v3/strokes",
    json={"strokes": strokes},
    headers=headers_mathpix,
)
print(json.dumps(r.json(), indent=4, sort_keys=True, ensure_ascii=False))