import sys, re, json, urllib.request, urllib.parse, time
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0',
    'Referer': 'https://www.grasen.com/',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://www.grasen.com',
}

# From JS: const N = `${r()}/${t.value}${A}` where r() = apiBase, t.value = 'en', A = '/article/detail'
# Try common API base URLs
SLUG = 'ev-charging-management-software-csms'

CANDIDATE_BASES = [
    'https://www.grasen.com',
    'https://api.grasen.com',
    'https://cms.grasen.com',
    'https://backend.grasen.com',
    'https://admin.grasen.com',
    'https://www.grasen.com/api',
]

for base in CANDIDATE_BASES:
    url = f'{base}/en/article/detail?slug={SLUG}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read().decode('utf-8', errors='replace')
            print(f'OK: {url}')
            print(f'  Status: {r.status}')
            print(f'  Data preview: {data[:300]}')
            break
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code}: {url}')
    except Exception as e:
        print(f'ERROR: {url} -> {e}')
    time.sleep(0.5)
