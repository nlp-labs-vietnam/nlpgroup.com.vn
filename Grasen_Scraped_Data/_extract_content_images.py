"""
Extract all images from article content (base64 data URIs + upload.grasen.com URLs).
Save base64 images as files. Update raw_articles txt with mappings.
Update xlsx Content Images column.
"""
import sys, re, json, os, base64, urllib.request, urllib.parse, time
sys.stdout.reconfigure(encoding='utf-8')

import openpyxl
from openpyxl.styles import Alignment

ARTICLES = [
    ("POST_001", "ev-charging-management-software-csms",                     "ev-charging-management-software"),
    ("POST_002", "are-all-electric-vehicle-chargers-the-same",               "are-all-electric-vehicle-chargers-the-same"),
    ("POST_003", "business-electric-car-charger-guide",                      "business-electric-car-charger-guide"),
    ("POST_004", "ev-charging-monetization-commercial-revenue",              "ev-charging-monetization"),
    ("POST_005", "top-dc-fast-charger-manufacturers-china-2026",             "top-10-dc-fast-charger-manufacturers-china"),
    ("POST_006", "how-to-use-grasen-app-ev-charging-management-for-payment", "how-to-use-grasen-app"),
    ("POST_007", "t480q-480kw-4-gun-dc-fast-charger",                       "grasen-t480q-480kw-4-gun-dc-fast-charger"),
    ("POST_008", "dual-gun-dc-fast-charger-power-sharing-grasen",           "dual-gun-dc-fast-charger-power-sharing"),
    ("POST_009", "ccs2-dc-fast-charger-commercial-ev-charging",             "ccs2-dc-fast-chargers-commercial-stations"),
    ("POST_010", "grasen-140th-canton-fair-2026",                           "grasen-canton-fair-140th-2026"),
]

IMG_HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.grasen.com/'}

def extract_images_from_content(content, local_folder, post_id):
    """Returns list of (source_ref, local_path, img_type)."""
    results = []
    
    # 1. Base64 data URIs  
    b64_imgs = re.finditer(r'src=["\']data:(image/[^;]+);base64,([A-Za-z0-9+/=]{100,})["\']', content)
    for i, m in enumerate(b64_imgs, 1):
        mime = m.group(1)  # e.g. image/png
        b64_data = m.group(2)
        ext = mime.split('/')[-1].replace('jpeg','jpg')
        local_path = f'images/{local_folder}/content_img_{i:02d}.{ext}'
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        try:
            img_bytes = base64.b64decode(b64_data)
            with open(local_path, 'wb') as f:
                f.write(img_bytes)
            results.append({
                'type': 'base64',
                'source': f'data:{mime};base64,...({len(b64_data)} chars)',
                'local': local_path,
                'size': len(img_bytes),
                'upload_url': None,
            })
            print(f"  Saved base64 img [{i}]: {local_path} ({len(img_bytes):,} bytes)")
        except Exception as e:
            print(f"  Base64 decode error [{i}]: {e}")
    
    # 2. upload.grasen.com CDN URLs
    cdn_imgs = re.findall(r'src=["\']https://upload\.grasen\.com/upload/([^"\'<>\s]+)["\']', content)
    for j, path in enumerate(cdn_imgs, len(results)+1):
        full_url = f'https://upload.grasen.com/upload/{path}'
        full_url = full_url.rstrip('.,;:)')
        ext_m = re.search(r'\.(png|jpg|jpeg|gif|webp)$', full_url, re.I)
        ext = ext_m.group(0) if ext_m else '.jpg'
        local_path = f'images/{local_folder}/content_img_{j:02d}{ext}'
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        enc_url = urllib.parse.quote(full_url, safe=':/?=&%')
        req = urllib.request.Request(enc_url, headers=IMG_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                img_bytes = r.read()
            with open(local_path, 'wb') as f:
                f.write(img_bytes)
            results.append({
                'type': 'cdn',
                'source': full_url,
                'local': local_path,
                'size': len(img_bytes),
                'upload_url': full_url,
            })
            print(f"  Downloaded CDN img [{j}]: {local_path} ({len(img_bytes):,} bytes)")
            time.sleep(0.8)
        except Exception as e:
            results.append({'type': 'cdn', 'source': full_url, 'local': local_path, 'error': str(e)})
            print(f"  CDN download failed [{j}]: {e}")
    
    return results

all_results = {}

for post_id, real_slug, local_folder in ARTICLES:
    print(f"\n{'='*60}")
    print(f"{post_id} | {real_slug}")
    
    api_file = f'_api_responses/{real_slug}.json'
    if not os.path.exists(api_file):
        print(f"  No API response file found")
        all_results[post_id] = {'error': 'no api response'}
        continue
    
    with open(api_file, encoding='utf-8') as f:
        data = json.load(f)
    
    article = data.get('data', {})
    content = article.get('content', '')
    cover   = article.get('cover', '')
    title   = article.get('title', '')
    pub_date = article.get('publishedTime', '')
    excerpt  = article.get('description', '')
    
    print(f"  Content: {len(content):,} chars")
    
    imgs = extract_images_from_content(content, local_folder, post_id)
    print(f"  Total images extracted: {len(imgs)}")
    
    # Build clean content images summary
    img_lines = []
    for im in imgs:
        if im['type'] == 'base64':
            img_lines.append(f"  [base64] → Local: {im['local']} ({im.get('size',0):,} bytes)")
        else:
            img_lines.append(f"  [cdn] URL: {im['source']}\n       Local: {im['local']}")
    
    all_results[post_id] = {
        'slug': real_slug,
        'local_folder': local_folder,
        'title': title,
        'excerpt': excerpt,
        'published_date': pub_date,
        'cover_url': cover,
        'images': imgs,
        'content_html_length': len(content),
    }
    
    # Update raw_articles txt
    txt_path = f'raw_articles/{local_folder}.txt'
    if os.path.exists(txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            existing = f.read()
        
        if img_lines:
            img_section = 'Content Images:\n' + '\n'.join(img_lines)
        else:
            img_section = 'Content Images: (article uses no embedded images — text only)'
        
        # Replace Content Images section  
        updated = re.sub(r'Content Images:.*$', img_section, existing, flags=re.DOTALL)
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f"  Updated: {txt_path}")

# Save final JSON map
with open('_image_map_complete.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2, default=str)
print("\nSaved: _image_map_complete.json")

# Update Excel file Content Images column
print("\nUpdating Grasen_News_Data.xlsx ...")
wb = openpyxl.load_workbook('Grasen_News_Data.xlsx')
ws = wb.active

post_to_row = {}
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    pid = row[0].value
    if pid:
        post_to_row[pid] = row

for post_id, data in all_results.items():
    if post_id not in post_to_row:
        continue
    row = post_to_row[post_id]
    imgs = data.get('images', [])
    
    # Column 11 = Thumbnail Local Path (index 10), Column 12 = Content Images (index 11)
    content_img_col = row[11]  # Content Images column
    
    if imgs:
        lines = []
        for im in imgs:
            if im['type'] == 'base64':
                lines.append(f"[base64] → {im['local']}")
            else:
                lines.append(f"{im['source']}\n→ {im['local']}")
        content_img_col.value = '\n'.join(lines)
    else:
        content_img_col.value = '(text only — no embedded images)'
    
    content_img_col.alignment = Alignment(vertical='top', wrap_text=True)
    
    # Also update Source URL with actual API slug
    source_url_col = row[5]  # Source URL column
    source_url_col.value = f"https://www.grasen.com/news/{data['slug']}"

wb.save('Grasen_News_Data.xlsx')
print("Excel updated: Grasen_News_Data.xlsx")

print("\n" + "="*70)
print("COMPLETE SUMMARY")
print("="*70)
for post_id, d in all_results.items():
    imgs = d.get('images', [])
    print(f"\n{post_id} | {d.get('slug','')}")
    print(f"  Content: {d.get('content_html_length',0):,} chars | Images: {len(imgs)}")
    for im in imgs:
        print(f"  → {im['local']}")
