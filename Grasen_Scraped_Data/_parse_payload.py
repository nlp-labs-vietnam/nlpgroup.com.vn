"""Parse Nuxt payload.json to extract article content images for each news post."""
import json, re, os, urllib.request, urllib.parse, time

with open(
    r"C:\Users\DELL\AppData\Local\Temp\bob-task-outputs\db84592159fd36a393636cc9738ff571\tool-outputs\tooluse_nwaXhiWxJNKza89qMUI2V1.txt",
    encoding="utf-8", errors="replace"
) as f:
    raw = f.read()

data = json.loads(raw)

# Nuxt payload is [{"data": 1, ...}, ["ShallowReactive", 2], {...map...}, ...]
# data[0] = meta/index map
# data[2] = key->index map for the flat array
# data[n] = actual values

flat = data  # the root is the flat array

# Get the key->index map (index 2 in the flat array)
key_map = flat[2]
print("Keys in payload:", list(key_map.keys())[:20])

# homeNewsList-  points to index 339
news_idx = key_map.get("homeNewsList-")
print(f"homeNewsList- index: {news_idx}")

news_data = flat[news_idx]
print(f"Type of news_data: {type(news_data)}")
print(f"News data preview: {str(news_data)[:500]}")
