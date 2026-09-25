#!/usr/bin/env python3
"""Pull verbatim prompt text for each entry from the author's own X post/reply (fxtwitter API)
and write data/prompts/<slug>.txt. Only text written by the post author is used; nothing is paraphrased.

Rules per entry (data/entries.json -> prompt):
  type=verbatim|excerpt|author_description : fetch `status` (author's post), cut between start_after / end_before
  type=repo_quotes : quote the author's messages as documented in the creator's GitHub README
  type=not_shared  : no file written; README shows "Not shared"
Cached fxtwitter JSON in --cache (fx-<id>.json / conv-<id>.json) is used when present.
"""
import json, os, re, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "proposals/2026-09-25/raw")
UA = {"User-Agent": "Mozilla/5.0"}

def status_text(sid, conv=None):
    for fn in (f"fx-{sid}.json",):
        p = os.path.join(CACHE, fn)
        if os.path.exists(p):
            return json.load(open(p))["tweet"]["text"]
    if conv:
        p = os.path.join(CACHE, f"conv-{conv}.json")
        if os.path.exists(p):
            d = json.load(open(p))
            for t in [d.get("status")] + (d.get("thread") or []) + (d.get("replies") or []):
                if t and t.get("id") == sid:
                    return t["text"]
    d = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://api.fxtwitter.com/i/status/{sid}", headers=UA)).read())
    return d["tweet"]["text"]

def cut(text, p):
    if p.get("start_after"):
        i = text.index(p["start_after"]); text = text[i + len(p["start_after"]):]
    if p.get("end_before"):
        j = text.rindex(p["end_before"]) if p.get("end_last") else text.index(p["end_before"])
        text = text[:j]
    return text.strip()

def repo_quotes(fn):
    s = open(os.path.join(CACHE, fn)).read()
    return "\n\n".join(q.strip() for q in re.findall(r'\*"(.+?)"\*', s))

def main():
    out = os.path.join(ROOT, "data/prompts"); os.makedirs(out, exist_ok=True)
    for e in json.load(open(os.path.join(ROOT, "data/entries.json"))):
        p = e["prompt"]
        if p["type"] == "not_shared":
            continue
        txt = repo_quotes(p["file"]) if p["type"] == "repo_quotes" else cut(status_text(p["status"], p.get("conv")), p)
        open(os.path.join(out, e["slug"] + ".txt"), "w").write(txt + "\n")
        print(f"{e['slug']}: {len(txt)} chars")

if __name__ == "__main__":
    main()
