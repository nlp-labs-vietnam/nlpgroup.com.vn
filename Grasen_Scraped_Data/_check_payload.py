import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# The saved per-article payload
with open('_payloads/ev-charging-management-software-csms.json', encoding='utf-8', errors='replace') as f:
    raw = f.read()

print(f"Payload size: {len(raw):,}")
print(f"First 200 chars: {raw[:200]}")
print()

# Look for API URL patterns
api_hits = re.findall(r'https?://[^\s"\'<>]{10,}', raw)
unique_apis = list(dict.fromkeys(api_hits))
print(f"URLs found: {len(unique_apis)}")
for u in unique_apis[:30]:
    print(f"  {u}")

# Look for content/article patterns
print()
content_hits = re.findall(r'"content"\s*:\s*"([^"]{200,})"', raw)
print(f"Content fields found: {len(content_hits)}")
for c in content_hits[:3]:
    print(f"  ...{c[:200]}...")
