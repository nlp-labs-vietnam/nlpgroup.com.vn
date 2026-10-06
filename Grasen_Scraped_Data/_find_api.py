import sys, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')

# Try to find the article detail API from the main Nuxt JS bundle
url = 'https://www.grasen.com/_nuxt/CGKkLKUb.js'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://www.grasen.com/'
})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        content = r.read().decode('utf-8', errors='replace')
    print(f"File size: {len(content):,}")
    
    # Search for API endpoint patterns
    for pat in [
        r'"/[a-z][^"]*(?:article|news|content|slug)[^"]{3,60}"',
        r'`\$\{[^`]*\}/[a-z][^`]*`',
        r'fetch\([^)]{20,100}\)',
        r'baseURL[^;]{5,50}',
    ]:
        m = re.findall(pat, content)
        if m:
            print(f"\nPattern {pat[:40]}:")
            for hit in m[:10]:
                print(f"  {hit}")
except Exception as e:
    print(f"Error: {e}")
