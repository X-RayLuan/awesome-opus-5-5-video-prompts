#!/usr/bin/env python3
"""Download an X post's video via the public fxtwitter API and build README assets.

Usage:
  python3 scripts/fetch_x_media.py <post_url> <slug> [--out DIR] [--max-seconds 170] [--target-mb 9.5]

Produces (under --out, default: repo root):
  assets/previews/<slug>.webp      1280px-wide still (from the X video thumbnail)
  assets/videos/<slug>-readme.mp4  H.264/AAC, faststart, <= target MB (GitHub/jsDelivr friendly)
  raw/<slug>-src.mp4               source download (gitignored)
Full originals stay on X; the README clip is a compressed preview only.
"""
import argparse, json, math, os, re, subprocess, sys, urllib.request

PREVIEW_SCALE = "scale=w='min(1280,iw)':h='min(720,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2"
UA = {"User-Agent": "Mozilla/5.0 (awesome-list media fetcher)"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()

def fx(post_url):
    m = re.search(r"(?:x|twitter)\.com/([^/]+)/status/(\d+)", post_url)
    if not m:
        sys.exit(f"not an X status url: {post_url}")
    return json.loads(get(f"https://api.fxtwitter.com/{m.group(1)}/status/{m.group(2)}"))["tweet"]

def pick_variant(video, max_h=1080):
    fmts = [f for f in video.get("formats", []) if ".mp4" in f.get("url", "") and ".m3u8" not in f["url"]]
    def h(f):  # short side, so vertical 1080x1920 counts as 1080p
        mm = re.search(r"/(\d+)x(\d+)/", f["url"])
        return min(int(mm.group(1)), int(mm.group(2))) if mm else 0
    ok = [f for f in fmts if h(f) <= max_h] or fmts
    ok.sort(key=lambda f: f.get("bitrate", 0))
    return ok[-1]["url"] if ok else video["url"]

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def probe_duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(out.strip())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post_url"); ap.add_argument("slug")
    ap.add_argument("--out", default=".")
    ap.add_argument("--max-seconds", type=float, default=170)
    ap.add_argument("--target-mb", type=float, default=9.5)
    ap.add_argument("--video-index", type=int, default=0)
    a = ap.parse_args()
    t = fx(a.post_url)
    vids = [m for m in (t.get("media") or {}).get("all", []) if m.get("type") in ("video", "gif")]
    if not vids:
        sys.exit("no video on post")
    v = vids[a.video_index]
    raw = os.path.join(a.out, "raw"); os.makedirs(raw, exist_ok=True)
    for d in ("assets/previews", "assets/videos"):
        os.makedirs(os.path.join(a.out, d), exist_ok=True)
    src = os.path.join(raw, f"{a.slug}-src.mp4")
    if not os.path.exists(src):
        open(src, "wb").write(get(pick_variant(v)))
    thumb = os.path.join(raw, f"{a.slug}-thumb.jpg")
    open(thumb, "wb").write(get(v["thumbnail_url"]))
    webp = os.path.join(a.out, "assets/previews", f"{a.slug}.webp")
    run(["ffmpeg", "-y", "-i", thumb, "-vf", PREVIEW_SCALE, "-quality", "78", webp])
    dur = min(probe_duration(src), a.max_seconds)
    has_audio = bool(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", src]).strip())
    abr = 96 if has_audio else 0
    vbr = int((a.target_mb * 0.94 * 8 * 1024) / dur) - abr  # kbit/s
    vbr = max(150, min(vbr, 2500))
    width = 1280 if vbr >= 900 else (960 if vbr >= 500 else 640)
    out = os.path.join(a.out, "assets/videos", f"{a.slug}-readme.mp4")
    base = ["ffmpeg", "-y", "-i", src, "-t", f"{dur:.2f}",
            "-vf", f"scale='min({width},iw)':-2",
            "-c:v", "libx264", "-preset", "slow", "-b:v", f"{vbr}k", "-maxrate", f"{int(vbr*1.5)}k", "-bufsize", f"{vbr*2}k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    base += (["-c:a", "aac", "-b:a", f"{abr}k"] if has_audio else ["-an"])
    run(["ffmpeg", "-y", "-i", src, "-t", f"{dur:.2f}", "-vf", f"scale='min({width},iw)':-2", "-c:v", "libx264",
         "-preset", "slow", "-b:v", f"{vbr}k", "-pass", "1", "-passlogfile", os.path.join(raw, a.slug), "-an", "-f", "mp4", os.devnull])
    run(base + ["-pass", "2", "-passlogfile", os.path.join(raw, a.slug), out])
    size = os.path.getsize(out) / 1e6
    print(json.dumps({"slug": a.slug, "author": t["author"]["screen_name"], "src_duration": round(probe_duration(src), 1),
                      "clip_seconds": round(dur, 1), "trimmed": dur < probe_duration(src) - 0.5, "readme_mp4_mb": round(size, 2),
                      "width": width, "vbr_k": vbr, "created_at": t.get("created_at"), "likes": t.get("likes"), "views": t.get("views")}))

if __name__ == "__main__":
    main()
