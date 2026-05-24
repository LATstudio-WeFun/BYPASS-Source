import requests
import re

url = "https://violated.lol/finished"

headers = {
    "referer": "https://linkvertise.com/"
}

res = requests.get(url, headers=headers)
match = re.search(r'<input id="keybox" value="([^"]+)"', res.text)

if match:
    print(f"key:{match.group(1)}")
else:
    print("key:not found")