import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

# Inspect POST_002 response (47KB - medium size, likely has images)
with open('_api_responses/are-all-electric-vehicle-chargers-the-same.json', encoding='utf-8') as f:
    data = json.load(f)

article = data['data']
content = article.get('content', '')
print(f"Content length: {len(content):,}")
print(f"\n--- First 2000 chars of content ---")
print(content[:2000])
print(f"\n--- Last 500 chars ---")
print(content[-500:])

# Search for img tags
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
print(f"\nImg src found: {len(imgs)}")
for img in imgs[:20]:
    print(f"  {img[:120]}")

# Search for background-image or url() patterns
bg_imgs = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', content)
print(f"\nbg url() found: {len(bg_imgs)}")
for img in bg_imgs[:10]:
    print(f"  {img[:120]}")
