"""
Fetch article detail via Nuxt server API.
From JS source: URL pattern is `${apiBase}/en/article/detail?slug=${slug}`
The apiBase is in runtimeConfig.public.apiBase — try to extract from __NUXT__ in HTML.
"""
import sys, re, json, urllib.request, time, os
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36',
    'Referer': 'https://www.grasen.com/',
    'Accept': 'text/html,application/xhtml+xml',
}

# First get the homepage to find __NUXT__ with apiBase
def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return None

# Fetch homepage HTML (raw, not rendered)
# The __NUXT__ script tag has the runtime config
homepage_html = fetch('https://www.grasen.com/')
if homepage_html:
    # Look for __NUXT_DATA__ or window.__NUXT__ with apiBase
    nuxt_match = re.search(r'window\.__NUXT__\s*=\s*({[^<]+})', homepage_html)
    if nuxt_match:
        print("Found window.__NUXT__:")
        print(nuxt_match.group(1)[:500])
    
    # Look for script with config
    config_match = re.search(r'"apiBase"\s*:\s*"([^"]+)"', homepage_html)
    if config_match:
        print(f"\napiBase from homepage: {config_match.group(1)}")
    
    # Look for nuxt script tags
    script_matches = re.findall(r'<script[^>]*>(.*?)</script>', homepage_html, re.DOTALL)
    for i, s in enumerate(script_matches):
        if 'apiBase' in s or 'public' in s.lower():
            print(f"\nScript {i} with apiBase/public:")
            print(s[:400])
            
    # Search raw for apiBase
    idx = homepage_html.find('apiBase')
    if idx >= 0:
        print(f"\napiBase context in homepage:")
        print(homepage_html[max(0,idx-100):idx+200])
    else:
        print("\napiBase NOT found in homepage HTML")
        
    # Look for NUXT_APP_BASE_URL or similar
    env_match = re.findall(r'(?:NUXT_APP|runtimeConfig|publicConfig|_APP_)[^"<]{10,100}', homepage_html)
    print("\nruntime config hits:")
    for h in env_match[:5]:
        print(f"  {h}")
