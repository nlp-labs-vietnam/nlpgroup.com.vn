import sys, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.grasen.com/'}
url = 'https://www.grasen.com/_nuxt/CJsLXv_D.js'
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as r:
    content = r.read().decode('utf-8', errors='replace')

# Find getArticleDetail context
idx = content.find('getArticleDetail')
if idx >= 0:
    print("getArticleDetail context:")
    print(content[max(0,idx-200):idx+400])
    print()

# Find all /cms/ paths
cms_paths = re.findall(r'"(/cms/[^"]{3,60})"', content)
print("\n/cms/ paths found:")
for p in list(dict.fromkeys(cms_paths)):
    print(f"  {p}")

# Find baseURL
base_hits = re.findall(r'baseURL[^,;]{5,80}', content)
print("\nbaseURL patterns:")
for h in base_hits[:10]:
    print(f"  {h}")

# Find all fetch/useFetch with URL patterns
fetch_hits = re.findall(r'(?:useFetch|fetch)\([`"\'][^`"\']{10,100}[`"\']', content)
print("\nfetch calls:")
for h in list(dict.fromkeys(fetch_hits))[:20]:
    print(f"  {h}")
