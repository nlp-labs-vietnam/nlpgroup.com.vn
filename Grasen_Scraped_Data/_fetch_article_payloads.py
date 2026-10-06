"""
Fetch each article's _payload.json from grasen.com to extract full content + images.
Article slugs and their URLs from homepage data.
"""
import json, os, time, re, urllib.request, urllib.parse

ARTICLES = [
    ("POST_001", "ev-charging-management-software"),
    ("POST_002", "are-all-electric-vehicle-chargers-the-same"),
    ("POST_003", "business-electric-car-charger-guide"),
    ("POST_004", "ev-charging-monetization"),
    ("POST_005", "top-10-dc-fast-charger-manufacturers-china"),
    ("POST_006", "how-to-use-grasen-app"),
    ("POST_007", "grasen-t480q-480kw-4-gun-dc-ev-fast-charger"),
    ("POST_008", "dual-gun-dc-fast-charger-power-sharing"),
    ("POST_009", "ccs2-dc-fast-chargers-commercial-stations"),
    ("POST_010", "grasen-canton-fair-140th-2026"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.grasen.com/",
}

def fetch_url(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None

def extract_images_from_html(html_content):
    """Extract all upload.grasen.com image URLs from HTML/JSON content."""
    pattern = r'https://upload\.grasen\.com/upload/[^\s\"\'\)\]>]+'
    imgs = list(dict.fromkeys(re.findall(pattern, html_content)))
    return imgs

results = {}

for post_id, slug in ARTICLES:
    print(f"\n{'='*60}")
    print(f"Fetching {post_id}: {slug}")
    
    # Step 1: GET the article HTML to find the payload fingerprint
    page_url = f"https://www.grasen.com/news/{slug}"
    html = fetch_url(page_url)
    time.sleep(1)
    
    if not html:
        print(f"  ERROR: Could not fetch {page_url}")
        results[slug] = {"error": "page fetch failed"}
        continue
    
    # Step 2: Find the payload URL from the HTML
    payload_match = re.search(r'href="(/_payload\.json\?[^"]+)"', html)
    if not payload_match:
        # Try another pattern
        payload_match = re.search(r'"(/_payload\.json\?[a-f0-9\-]+)"', html)
    
    if payload_match:
        payload_path = payload_match.group(1)
        payload_url = f"https://www.grasen.com{payload_path}"
        print(f"  Payload URL: {payload_url}")
        
        payload_raw = fetch_url(payload_url)
        time.sleep(1.5)
        
        if payload_raw:
            # Save raw payload for inspection
            out_dir = f"_payloads"
            os.makedirs(out_dir, exist_ok=True)
            with open(f"{out_dir}/{slug}.json", "w", encoding="utf-8") as f:
                f.write(payload_raw)
            print(f"  Saved payload ({len(payload_raw):,} chars)")
            
            # Extract all grasen upload images from payload
            imgs = extract_images_from_html(payload_raw)
            print(f"  Found {len(imgs)} images: {imgs[:3]}")
            results[slug] = {"payload_url": payload_url, "images": imgs}
        else:
            print(f"  ERROR: Could not fetch payload")
            results[slug] = {"error": "payload fetch failed"}
    else:
        # Still try to extract images from the HTML itself
        imgs = extract_images_from_html(html)
        print(f"  No payload URL found. Images in HTML: {len(imgs)}")
        results[slug] = {"payload_url": None, "images": imgs}

# Print summary
print("\n\n" + "="*60)
print("SUMMARY: Images per article")
print("="*60)
for slug, data in results.items():
    imgs = data.get("images", [])
    print(f"\n{slug}: {len(imgs)} images")
    for i, img in enumerate(imgs):
        print(f"  [{i+1}] {img}")

# Save results
with open("_image_map.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\nSaved: _image_map.json")
