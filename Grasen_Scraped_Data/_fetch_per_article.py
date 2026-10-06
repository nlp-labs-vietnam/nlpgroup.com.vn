"""
Fetch per-article Nuxt payload using correct slugs from homepage data.
Extract: full HTML content, all content images (upload.grasen.com).
"""
import json, sys, re, os, time, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

# Correct slugs from homepage payload + their POST IDs and local folder names
ARTICLES = [
    ("POST_001", "ev-charging-management-software-csms",            "ev-charging-management-software"),
    ("POST_002", "are-all-electric-vehicle-chargers-the-same",       "are-all-electric-vehicle-chargers-the-same"),
    ("POST_003", "business-electric-car-charger-guide",              "business-electric-car-charger-guide"),
    ("POST_004", "ev-charging-monetization-commercial-revenue",      "ev-charging-monetization"),
    ("POST_005", "top-dc-fast-charger-manufacturers-china-2026",     "top-10-dc-fast-charger-manufacturers-china"),
    ("POST_006", "how-to-use-grasen-app-ev-charging-management-for-payment", "how-to-use-grasen-app"),
    ("POST_007", "t480q-480kw-4-gun-dc-fast-charger",               "grasen-t480q-480kw-4-gun-dc-fast-charger"),
    ("POST_008", "dual-gun-dc-fast-charger-power-sharing-grasen",   "dual-gun-dc-fast-charger-power-sharing"),
    ("POST_009", "ccs2-dc-fast-charger-commercial-ev-charging",     "ccs2-dc-fast-chargers-commercial-stations"),
    ("POST_010", "grasen-140th-canton-fair-2026",                   "grasen-canton-fair-140th-2026"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Referer": "https://www.grasen.com/",
}
HEADERS_JSON = {**HEADERS, "Accept": "application/json"}

def fetch(url, headers=HEADERS):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"    FETCH ERROR: {e}")
        return None

def extract_img_urls(text):
    pat = r'https://upload\.grasen\.com/upload/[^\s"\'\\<>{}|\[\]`\^)]+'
    found = re.findall(pat, text)
    # clean trailing punctuation
    cleaned = []
    for u in found:
        u = u.rstrip('.,;:!?)"\'')
        if re.search(r'\.(png|jpg|jpeg|gif|webp)$', u, re.I):
            cleaned.append(u)
    return list(dict.fromkeys(cleaned))

results = {}
os.makedirs("_payloads", exist_ok=True)

for post_id, real_slug, local_folder in ARTICLES:
    print(f"\n{'='*60}")
    print(f"{post_id} | slug: {real_slug}")
    
    page_url = f"https://www.grasen.com/news/{real_slug}"
    html = fetch(page_url)
    time.sleep(1.5)
    
    if not html:
        results[post_id] = {"slug": real_slug, "error": "page fetch failed"}
        continue
    
    # Find payload fingerprint in HTML
    payload_match = re.search(r'"(/_payload\.json\?[a-f0-9\-]+)"', html)
    if not payload_match:
        payload_match = re.search(r"'(/_payload\.json\?[a-f0-9\-]+)'", html)
    
    if not payload_match:
        print(f"  No payload URL found in HTML")
        # Still try to extract images from page HTML
        imgs = extract_img_urls(html)
        results[post_id] = {"slug": real_slug, "payload_url": None, "images": imgs}
        continue
    
    payload_path = payload_match.group(1)
    payload_url = f"https://www.grasen.com{payload_path}"
    fingerprint = payload_path.split("?")[1]
    print(f"  Payload fingerprint: {fingerprint}")
    
    payload_raw = fetch(payload_url, headers=HEADERS_JSON)
    time.sleep(1.5)
    
    if not payload_raw:
        results[post_id] = {"slug": real_slug, "error": "payload fetch failed"}
        continue
    
    # Save payload
    with open(f"_payloads/{real_slug}.json", "w", encoding="utf-8") as f:
        f.write(payload_raw)
    print(f"  Payload size: {len(payload_raw):,} chars")
    
    # Try to parse as Nuxt flat array and find content
    content_html = None
    try:
        flat = json.loads(payload_raw)
        # Search for content field — look for HTML strings with <p> or <img> tags
        for i, item in enumerate(flat):
            if isinstance(item, str) and len(item) > 500 and ('<p>' in item or '<img' in item or '<h2' in item):
                print(f"  Found content at flat[{i}] len={len(item)}")
                content_html = item
                break
        
        # Also look for article-specific images
        all_imgs_in_payload = extract_img_urls(payload_raw)
        print(f"  Total images in payload: {len(all_imgs_in_payload)}")
        
        # Separate thumbnail (already known) from content images
        # Content images are usually different from cover
        cover_imgs = [u for u in all_imgs_in_payload if any(kw in u for kw in [
            '20260930', '20260928', '20260924', '20260923', '20260922',
            '20260918', '20260915', '20260912', '20260909', '20260910'
        ])]
        
        results[post_id] = {
            "slug": real_slug,
            "local_folder": local_folder,
            "payload_url": payload_url,
            "payload_fingerprint": fingerprint,
            "has_content": content_html is not None,
            "content_length": len(content_html) if content_html else 0,
            "all_images": all_imgs_in_payload,
            "content_html_preview": content_html[:500] if content_html else None,
        }
        
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        imgs = extract_img_urls(payload_raw)
        results[post_id] = {"slug": real_slug, "error": f"json parse: {e}", "images": imgs}

# Print summary
print("\n\n" + "="*70)
print("SUMMARY")
print("="*70)
for post_id, data in results.items():
    print(f"\n{post_id} | {data.get('slug','?')}")
    print(f"  Content found: {data.get('has_content', False)} | len={data.get('content_length', 0)}")
    imgs = data.get("all_images", [])
    print(f"  Images ({len(imgs)}): {imgs[:4]}")

with open("_image_map_v2.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\nSaved: _image_map_v2.json")
