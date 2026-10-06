import sys, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.grasen.com/'}
url = 'https://www.grasen.com/_nuxt/CJsLXv_D.js'
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as r:
    content = r.read().decode('utf-8', errors='replace')

# Find the s() function that wraps fetch — look for its definition near the api calls
idx = content.find('getArticleDetail:async b=>s(')
print(f"API def at index: {idx}")
# Look back 2000 chars for the s= definition
chunk = content[max(0,idx-2000):idx+200]
print(chunk[-1000:])
print()

# Search for NUXT_APP_API or similar env config
env_hits = re.findall(r'(?:NUXT_APP|API_URL|api_url|apiUrl|_apiBase)[^;,\n"\']{3,80}', content)
print("Env/API config hits:")
for h in env_hits[:10]:
    print(f"  {h}")

# Search for https:// api domain
https_hits = re.findall(r'"https://[^"]{10,60}/(?:api|article|cms)[^"]{0,40}"', content)
print("\nhttps API URL strings:")
for h in list(dict.fromkeys(https_hits))[:15]:
    print(f"  {h}")
