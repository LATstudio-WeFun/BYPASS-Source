# Rocketscriptz Bypass / BY BYPASS.LAT(ilat)
# python rocketscriptz.py {url}
import sys, requests, re

html = requests.get(sys.argv[1], verify=False).text
m = re.search(r'id="textToCopy"[^>]*>(.*?)</div>', html, re.S)
print(m.group(1).strip() if m else "")
