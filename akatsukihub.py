# Akatsukihub Bypass / BY BYPASS.LAT(ilat)
import re
import time
from curl_cffi import requests


def get_key(retries=5, delay=10):
    session = requests.Session(impersonate="chrome")
    for _ in range(retries):
        try:
            session.get("https://akatsukihub.com/", timeout=20)
            r = session.get(
                "https://akatsukihub.com/Get-Key",
                headers={"Referer": "https://linkvertise.com/"},
                timeout=20,
            )
            m = re.search(r'navigator\.clipboard\.writeText\("([^"]+)"\)', r.text)
            if not m:
                m = re.search(r'id="dynamicKey">([^<]+)<', r.text)
            if m:
                key = m.group(1)
                exp = re.search(r'new Date\("([^"]+)"\)', r.text)
                expires = exp.group(1) if exp else None
                return key, expires
        except Exception:
            time.sleep(delay)
    return None, None


if __name__ == "__main__":
    key, expires = get_key()
    if key:
        print(f"Key: {key}")
        if expires:
            print(f"Expires: {expires}")
    else:
        print("Failed to get key")