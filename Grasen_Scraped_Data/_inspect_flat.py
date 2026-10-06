"""
Read flat[340..424] directly from homepage Nuxt payload to get raw news article data.
No recursive resolve — just look at what's at each index directly.
"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(
    r"C:\Users\DELL\AppData\Local\Temp\bob-task-outputs\db84592159fd36a393636cc9738ff571\tool-outputs\tooluse_nwaXhiWxJNKza89qMUI2V1.txt",
    encoding="utf-8", errors="replace"
) as f:
    raw = f.read()

flat = json.loads(raw)

# homeNewsList- = index 339 → list of 10 article indices
news_indices = flat[339]  # [340, 349, 357, ...]
print(f"Article indices: {news_indices}\n")

def extract_imgs(s):
    return re.findall(r'https://upload\.grasen\.com/upload/[^\s"\'<>]+', str(s))

for art_idx in news_indices:
    raw_art = flat[art_idx]
    print(f"\n--- flat[{art_idx}] ---")
    print(f"Type: {type(raw_art)}")
    if isinstance(raw_art, dict):
        for k, v in raw_art.items():
            # Don't resolve, just print the raw value (int ref or actual value)
            val_preview = str(v)[:120]
            print(f"  {k!r}: {val_preview}")
            # If value is an int, look it up one level (no recursion)
            if isinstance(v, int) and v < len(flat):
                child = flat[v]
                if isinstance(child, str):
                    print(f"    → (str) {child[:120]}")
                elif isinstance(child, dict):
                    print(f"    → (dict keys) {list(child.keys())}")
                elif isinstance(child, list):
                    print(f"    → (list len={len(child)}) {str(child[:3])[:120]}")
    elif isinstance(raw_art, list):
        print(f"  List items: {raw_art[:5]}")
    else:
        print(f"  Value: {str(raw_art)[:200]}")
