# Link4Sub Bypass / BY BYPASS.LAT(ilat)
# python link4sub.py {url}
import json, sys
from urllib.request import Request, urlopen

alias = sys.argv[1].rstrip("/").split("/")[-1]
req = Request(f"https://link4sub.com/api/{alias}/fetch-data?lang=en",
              headers={"User-Agent": "Mozilla/5.0"})
with urlopen(req) as r:
    lnk = json.load(r)["data"]["data"]["lnk"]
print("\n".join(v["url"] for v in lnk.values()))