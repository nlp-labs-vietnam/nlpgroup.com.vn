"""
Fetch all 10 articles via Grasen API: GET https://grasen.com/api/en/article/detail?slug={slug}
Extract: full HTML content, all content image URLs, then download content images.
"""
import sys, re, json, urllib.request, urllib.parse, time, os
sys.stdout.reconfigure(encoding='utf-8')

API_BASE = 'https://grasen.com/api'
LANG = 'en'

ARTICLES = [
    ("POST_001", "ev-charging-management-software-csms",                    "ev-charging-management-software"),
    ("POST_002", "are-all-electric-vehicle-chargers-the-same",              "are-all-electric-vehicle-chargers-the-same"),
    ("POST_003", "business-electric-car-charger-guide",                     "business-electric-car-charger-guide"),
    ("POST_004", "ev-charging-monetization-commercial-revenue",             "ev-charging-monetization"),
    ("POST_005", "top-dc-fast-charger-manufacturers-china-2026",            "top-10-dc-fast-charger-manufacturers-china"),
    ("POST_006", "how-to-use-grasen-app-ev-charging-management-for-payment","how-to-use-grasen-app"),
    ("POST_007", "t480q-480kw-4-gun-dc-fast-charger",                      "grasen-t480q-480kw-4-gun-dc-fast-charger"),
    ("POST_008", "dual-gun-dc-fast-charger-power-sharing-grasen",          "dual-gun-dc-fast-charger-power-sharing"),
    ("POST_009", "ccs2-dc-fast-charger-commercial-ev-charging",            "ccs2-dc-fast-chargers-commercial-stations"),
    ("POST_010", "grasen-140th-canton-fair-2026",                          "grasen-canton-fair-140th-2026"),
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
    'Referer': 'https://www.grasen.com/',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.grasen.com',
}
IMG_HEADERS = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.grasen.com/',
}

def fetch_json(slug):
    url = f'{API_BASE}/{LANG}/article/detail?slug={urllib.parse.quote(slug)}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode('utf-8', errors='replace'))
    except Exception as e:
        print(f'  ERROR: {e}')
        return None

def extract_imgs(html_content):
    """Extract all upload.grasen.com image URLs from HTML content."""
    pat = r'https://upload\.grasen\.com/upload/[^\s"\'<>\\(){}]+'
    found = re.findall(pat, html_content)
    cleaned = []
    for u in found:
        u = re.sub(r'[.,;:!?"\')\]>]+$', '', u)
        if re.search(r'\.(png|jpg|jpeg|gif|webp)$', u, re.I):
            cleaned.append(u)
    return list(dict.fromkeys(cleaned))

def download_image(url, local_path):
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    enc_url = urllib.parse.quote(url, safe=':/?=&%')
    req = urllib.request.Request(enc_url, headers=IMG_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(local_path, 'wb') as f:
            f.write(data)
        return len(data)
    except Exception as e:
        return f'ERROR: {e}'

results = {}

for post_id, real_slug, local_folder in ARTICLES:
    print(f"\n{'='*60}")
    print(f"{post_id} | {real_slug}")
    
    data = fetch_json(real_slug)
    time.sleep(1.5)
    
    if not data:
        results[post_id] = {'slug': real_slug, 'error': 'fetch failed'}
        continue
    
    print(f"  Response keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
    
    # Save raw API response
    os.makedirs('_api_responses', exist_ok=True)
    with open(f'_api_responses/{real_slug}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Extract article data
    article = data.get('data') or data.get('result') or data
    if isinstance(article, dict):
        title   = article.get('title', '')
        content = article.get('content', '') or ''
        cover   = article.get('cover', '')
        pub_date = article.get('publishedTime', '')
        excerpt  = article.get('description', '')
        
        print(f"  Title: {title[:80]}")
        print(f"  Content length: {len(content):,} chars")
        print(f"  Cover: {cover[:80]}")
        
        # Extract all images from content HTML
        content_imgs = extract_imgs(content)
        print(f"  Content images: {len(content_imgs)}")
        for img in content_imgs:
            print(f"    {img}")
        
        # Download content images
        downloaded = []
        for i, img_url in enumerate(content_imgs, 1):
            ext = re.search(r'\.(png|jpg|jpeg|gif|webp)$', img_url, re.I)
            ext = ext.group(0) if ext else '.jpg'
            local_path = f'images/{local_folder}/content_img_{i:02d}{ext}'
            result = download_image(img_url, local_path)
            if isinstance(result, int):
                print(f"    Downloaded: {local_path} ({result:,} bytes)")
                downloaded.append({'url': img_url, 'local': local_path, 'size': result})
            else:
                print(f"    FAILED: {local_path} → {result}")
                downloaded.append({'url': img_url, 'local': local_path, 'error': result})
            time.sleep(0.8)
        
        results[post_id] = {
            'slug': real_slug,
            'local_folder': local_folder,
            'title': title,
            'excerpt': excerpt,
            'published_date': pub_date,
            'cover_url': cover,
            'content_images': [d['url'] for d in downloaded],
            'content_images_local': downloaded,
            'content_html_length': len(content),
        }
        
        # Update the raw_articles txt file with real content + image URLs
        txt_path = f'raw_articles/{local_folder}.txt'
        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                existing = f.read()
            # Replace "Content Images: (none extracted — JS-rendered page)" with real images
            img_block = '\n'.join([f'  [{j+1}] URL: {d["url"]}\n       Local: {d["local"]}' 
                                   for j, d in enumerate(downloaded)])
            img_section = f'Content Images:\n{img_block}' if img_block else 'Content Images: (none in article content)'
            updated = re.sub(r'Content Images:.*', img_section, existing, flags=re.DOTALL)
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"  Updated: {txt_path}")
    else:
        print(f"  Unexpected response format: {str(article)[:200]}")
        results[post_id] = {'slug': real_slug, 'error': 'unexpected format', 'raw': str(article)[:500]}

# Save full results map
with open('_image_map_final.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\n\nSaved: _image_map_final.json")

# Print final summary
print("\n" + "="*70)
print("FINAL SUMMARY: Content Images per Article")
print("="*70)
for post_id, d in results.items():
    imgs = d.get('content_images', [])
    print(f"\n{post_id} | {d.get('slug','')}")
    print(f"  Thumbnail: {d.get('cover_url','')[:80]}")
    if imgs:
        for i, url in enumerate(imgs, 1):
            print(f"  [{i}] {url}")
    else:
        print("  (no content images)")
