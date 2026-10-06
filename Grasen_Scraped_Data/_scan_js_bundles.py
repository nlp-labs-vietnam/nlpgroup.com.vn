import sys, re, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')

# Fetch all preloaded JS modules from homepage HTML and search for API endpoints
JS_FILES = [
    'CJsLXv_D.js',   # main bundle (large)
    'BDryWUt8.js',
    '3ugIAeiH.js',
    'cOPsimbB.js',
    'DyPlsPQw.js',
]

HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.grasen.com/'}

API_PATTERNS = [
    r'/cms/[a-zA-Z/]{5,50}',
    r'/api/[a-zA-Z/]{5,50}',
    r'slug[^"]{3,30}',
    r'article[A-Za-z]*[Dd]etail',
    r'newsDetail',
    r'getArticle',
    r'contentDetail',
]

for js_file in JS_FILES:
    url = f'https://www.grasen.com/_nuxt/{js_file}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            content = r.read().decode('utf-8', errors='replace')
        print(f"\n{'='*50}")
        print(f"{js_file} ({len(content):,} chars)")
        for pat in API_PATTERNS:
            hits = list(dict.fromkeys(re.findall(pat, content)))
            if hits:
                print(f"  [{pat[:30]}]: {hits[:5]}")
    except Exception as e:
        print(f"  Error {js_file}: {e}")
    time.sleep(0.5)
