"""Download thumbnail images for all 10 Grasen articles."""
import urllib.request
import os
import time

images = [
    (
        "https://upload.grasen.com/upload/2026/09/30/EV Charging Management Software_20260930103919A129.png",
        "images/ev-charging-management-software/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/28/All Electric Vehicle Chargers the Same？1_20260928140207A128.jpg",
        "images/are-all-electric-vehicle-chargers-the-same/cover.jpg",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/24/T480000_20260924162451A126.png",
        "images/business-electric-car-charger-guide/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/23/EV Charging Monetization picture_20260923095216A122.png",
        "images/ev-charging-monetization/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/22/Top 10 DC Fast Charger Manufacturer_20260922140219A121.png",
        "images/top-10-dc-fast-charger-manufacturers-china/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/18/Explore Grasen EV Charging Solutions_20260918114725A119.png",
        "images/how-to-use-grasen-app/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/23/480kW 4-Gun DC EV Fast Charger picture_20260923102825A123.png",
        "images/grasen-t480q-480kw-4-gun-dc-fast-charger/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/15/文章配图1)_20260915152149A115.jpg",
        "images/dual-gun-dc-fast-charger-power-sharing/cover.jpg",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/12/文章配图3_20260912085619A114.png",
        "images/ccs2-dc-fast-chargers-commercial-stations/cover.png",
    ),
    (
        "https://upload.grasen.com/upload/2026/09/10/广交会官网_20260910145319A112.jpg",
        "images/grasen-canton-fair-140th-2026/cover.jpg",
    ),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Referer": "https://www.grasen.com/",
}

ok = 0
fail = 0
for url, local_path in images:
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    encoded_url = urllib.parse.quote(url, safe=":/?=&%")
    req = urllib.request.Request(encoded_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        with open(local_path, "wb") as f:
            f.write(data)
        print(f"  OK  {local_path}  ({len(data):,} bytes)")
        ok += 1
    except Exception as e:
        print(f"  FAIL {local_path}: {e}")
        fail += 1
    time.sleep(1.5)

print(f"\nDone: {ok} downloaded, {fail} failed.")
