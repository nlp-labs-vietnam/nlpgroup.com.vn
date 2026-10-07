"""
Remove white background from thumbnail.png using flood-fill from corners.
Handles anti-aliased edges with tolerance-based alpha blending.
"""
from PIL import Image
import sys, shutil

sys.stdout.reconfigure(encoding='utf-8')

def remove_bg_floodfill(src_path, dst_path, tolerance=30):
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    pixels = img.load()

    # Collect seed pixels from all 4 corners
    seeds = [(0,0),(w-1,0),(0,h-1),(w-1,h-1)]
    # Also sample edges
    for x in range(0, w, 10):
        seeds.append((x, 0))
        seeds.append((x, h-1))
    for y in range(0, h, 10):
        seeds.append((0, y))
        seeds.append((w-1, y))

    # Get background color from top-left corner
    bg_r, bg_g, bg_b, _ = pixels[0, 0]

    def color_distance(px):
        r, g, b, a = px
        return abs(int(r)-bg_r) + abs(int(g)-bg_g) + abs(int(b)-bg_b)

    # BFS flood fill
    visited = [[False]*h for _ in range(w)]
    queue = []
    for sx, sy in seeds:
        if not visited[sx][sy] and color_distance(pixels[sx,sy]) <= tolerance*3:
            queue.append((sx,sy))
            visited[sx][sy] = True

    # Mark background pixels
    bg_mask = [[False]*h for _ in range(w)]
    while queue:
        x, y = queue.pop()
        bg_mask[x][y] = True
        for nx, ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if 0<=nx<w and 0<=ny<h and not visited[nx][ny]:
                if color_distance(pixels[nx,ny]) <= tolerance*3:
                    visited[nx][ny] = True
                    queue.append((nx,ny))

    # Apply transparency with soft edge blending
    result = img.copy()
    res_px = result.load()
    for x in range(w):
        for y in range(h):
            if bg_mask[x][y]:
                res_px[x, y] = (bg_r, bg_g, bg_b, 0)
            else:
                # Check if near background — apply partial alpha for anti-aliasing
                px = pixels[x, y]
                dist = color_distance(px)
                if dist < tolerance:
                    # Smooth transition
                    alpha = int(255 * (dist / tolerance))
                    res_px[x, y] = (px[0], px[1], px[2], alpha)

    result.save(dst_path, "PNG")
    print(f"  Saved: {dst_path}  ({w}x{h})")
    return result

print("Removing white background from thumbnail.png ...")
remove_bg_floodfill("build/img/thumbnail.png", "build/img/thumbnail.png", tolerance=25)
remove_bg_floodfill("build/img/thumbnail.png", "src/img/thumbnail.png", tolerance=25)

print("\nCopying ologreen.png as official logos ...")
import os
def save_resized(src, dst, size=None):
    img = Image.open(src).convert("RGBA")
    if size:
        img = img.resize(size, Image.LANCZOS)
    img.save(dst, "PNG")
    print(f"  {dst}  {img.size}")

save_resized("ologreen.png", "build/img/logo.png")
save_resized("ologreen.png", "build/img/logo-white.png")
save_resized("ologreen.png", "src/img/logo.png")
save_resized("ologreen.png", "src/img/logo-white.png")
save_resized("ologreen.png", "build/img/favicon-32x32.png",          (32,32))
save_resized("ologreen.png", "build/img/favicon-16x16.png",          (16,16))
save_resized("ologreen.png", "build/img/apple-touch-icon.png",       (180,180))
save_resized("ologreen.png", "build/img/android-chrome-192x192.png", (192,192))
save_resized("ologreen.png", "build/img/android-chrome-512x512.png", (512,512))
save_resized("ologreen.png", "build/img/mstile-150x150.png",         (150,150))
save_resized("ologreen.png", "src/img/favicon-32x32.png",            (32,32))
save_resized("ologreen.png", "src/img/favicon-16x16.png",            (16,16))
save_resized("ologreen.png", "src/img/apple-touch-icon.png",         (180,180))
shutil.copy("ologreen.png", "build/img/vnegreen-logo.png")
shutil.copy("ologreen.png", "src/img/vnegreen-logo.png")
print("  build/img/vnegreen-logo.png")

print("\nDone.")
