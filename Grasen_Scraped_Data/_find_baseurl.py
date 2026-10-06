import sys, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.grasen.com/'}
url = 'https://www.grasen.com/_nuxt/CJsLXv_D.js'
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as r:
    content = r.read().decode('utf-8', errors='replace')

# Find Eg() definition
idx = content.find('function Eg(')
if idx < 0:
    idx = content.find('Eg=')
if idx < 0:
    idx = content.find('const Eg')
print(f"Eg found at: {idx}")
print(content[max(0,idx-100):idx+300])
print()

# Also search for the API base URL pattern
hits = re.findall(r'(?:apiBase|API_BASE|baseUrl|NUXT_API)[^;,\n]{5,80}', content)
print("Base URL patterns:")
for h in hits[:10]:
    print(f"  {h}")

# Search for https:// in function context near article
idx2 = content.find('/article/detail')
print(f"\n/article/detail context:")
print(content[max(0,idx2-300):idx2+200])
