# BloxHub Bypass / BY ilat

import requests
import re
import time
import sys

BloxHub = "https://bloxhub.click"
BloxHub_API = f"{BloxHub}/api/get-free-key.php"
BloxHub_GetKeyPage = f"{BloxHub}/get-key.php"

BloxHub_BrowserHeaders = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

BloxHub_APIHeaders = {
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

W = "\033[97m"
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
C = "\033[96m"
E = "\033[0m"


def log(tag, msg, color=W):
    print(f"  {color}[{tag}]{E} {msg}")


def generateKey():
    print(f"\n  {C}BloxHub Bypass / BY ilat{E}\n")

    s = requests.Session()
    s.headers.update(BloxHub_BrowserHeaders)

    log("init", "fetching page ...", C)
    r = s.get(BloxHub_GetKeyPage)
    if r.status_code != 200:
        log("err", f"page returned {r.status_code}", R)
        return None

    m = re.search(r'freeKeyToken\s*=\s*"([^"]+)"', r.text)
    if not m:
        log("err", "freeKeyToken not found", R)
        return None
    freeKeyToken = m.group(1)
    log("token", freeKeyToken, Y)

    hdr = {
        **BloxHub_APIHeaders,
        "X-Free-Key-Token": freeKeyToken,
        "Referer": BloxHub_GetKeyPage,
        "Origin": BloxHub,
    }

    log("step", "goToStep2 ...", C)
    r = s.get(f"{BloxHub_API}?action=set_step&step=2", headers=hdr)
    d = r.json()
    if not d.get("success"):
        log("err", d.get("message", "unknown"), R)
        return None

    log("step", "goToStep3 ...", C)
    r = s.get(f"{BloxHub_API}?action=set_step&step=3", headers=hdr)
    d = r.json()
    if not d.get("success"):
        log("err", d.get("message", "unknown"), R)
        return None

    log("wait", "15s server timer ...", Y)
    for i in range(15, 0, -1):
        sys.stdout.write(f"\r  {Y}[wait]{E} {i}s ...")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write(f"\r  {G}[wait]{E} done.        \n")

    log("key", "requesting ...", C)
    r = s.get(BloxHub_API, headers=hdr)
    d = r.json()

    if d.get("success"):
        key = d["key"]
        exp = d.get("expires", "n/a")
        log("ok", f"{G}{key}{E}  exp: {exp}", G)
        return {"key": key, "expires": exp}

    log("err", d.get("message", "unknown"), R)
    return None


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("-n", "--count", type=int, default=1)
    args = p.parse_args()

    keys = []
    for i in range(args.count):
        if i > 0:
            print()
        r = generateKey()
        if r:
            keys.append(r)

    print(f"\n  {'─' * 36}")
    for k in keys:
        print(f"  {G}{k['key']}{E}  exp: {k['expires']}")
    print(f"  got {len(keys)} key(s)")