import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

PAYLOAD_FILE = r"C:\Users\DELL\AppData\Local\Temp\bob-task-outputs\db84592159fd36a393636cc9738ff571\tool-outputs\tooluse_nwaXhiWxJNKza89qMUI2V1.txt"
with open(PAYLOAD_FILE, encoding='utf-8', errors='replace') as f:
    raw = f.read()

# Search for apiBase
hits = re.findall(r'apiBase[^\s,;"]{3,80}', raw)
print('apiBase hits:')
for h in hits[:10]:
    print(f'  {h}')

# Search for the config object with public key  
hits2 = re.findall(r'"apiBase":"[^"]{5,80}"', raw)
print('\napiBase values:')
for h in hits2[:5]:
    print(f'  {h}')

# Broader: find any https:// url in the flat array items
flat = json.loads(raw)
for i, v in enumerate(flat):
    if isinstance(v, str) and 'http' in v and 'grasen' in v.lower() and i < 20:
        print(f'flat[{i}]: {v[:150]}')

# The en-config key
key_map = flat[2]
config_idx = key_map.get('en-config}')
print(f"\nen-config index: {config_idx}")
if config_idx:
    cfg = flat[config_idx]
    print(f"Config type: {type(cfg)}")
    if isinstance(cfg, dict):
        for k,v in cfg.items():
            print(f"  {k}: {str(v)[:100]}")
