"""
Parse homepage payload to extract article content + images for each news post.
The homepage Nuxt payload contains ALL 10 news article data in homeNewsList.
"""
import json, os, sys, re

sys.stdout.reconfigure(encoding='utf-8')

with open(
    r"C:\Users\DELL\AppData\Local\Temp\bob-task-outputs\db84592159fd36a393636cc9738ff571\tool-outputs\tooluse_nwaXhiWxJNKza89qMUI2V1.txt",
    encoding="utf-8", errors="replace"
) as f:
    raw = f.read()

flat = json.loads(raw)

# flat[2] is the key->index map
key_map = flat[2]
news_idx = key_map["homeNewsList-"]
news_list_indices = flat[news_idx]  # list of indices

print(f"Number of articles: {len(news_list_indices)}")

def resolve(val, flat):
    """Recursively resolve indices in flat array."""
    if isinstance(val, int) and val < len(flat):
        return resolve(flat[val], flat)
    elif isinstance(val, list):
        return [resolve(v, flat) for v in val]
    elif isinstance(val, dict):
        return {k: resolve(v, flat) for k, v in val.items()}
    return val

def extract_img_urls(text):
    if not isinstance(text, str):
        return []
    return list(dict.fromkeys(re.findall(r'https://upload\.grasen\.com/upload/\S+?\.(png|jpg|jpeg|gif|webp)', text, re.IGNORECASE)))

articles_data = []
for i, art_idx in enumerate(news_list_indices):
    art_raw = flat[art_idx]
    if isinstance(art_raw, dict):
        art = {k: resolve(v, flat) for k, v in art_raw.items()}
    elif isinstance(art_raw, int):
        art = resolve(art_raw, flat)
    else:
        art = art_raw
    articles_data.append(art)

for i, art in enumerate(articles_data):
    print(f"\n{'='*60}")
    print(f"Article {i+1}")
    if isinstance(art, dict):
        for k, v in art.items():
            val_str = str(v)[:200]
            print(f"  {k}: {val_str}")
    else:
        print(f"  Raw: {str(art)[:300]}")
