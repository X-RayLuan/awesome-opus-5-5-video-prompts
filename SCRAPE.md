# Daily scrape playbook — Awesome Opus 5.5 Video Prompts

How the seed batch (2026-09-25) was built and how a daily job should continue it. Mirrors the
`proposals/<date>/` flow used by [awesome-gpt-6-astra-prompts](https://github.com/X-RayLuan/awesome-gpt-6-astra-prompts).
**Never push or open a PR without owner approval.** A daily run only writes `proposals/<YYYY-MM-DD>/`.

## What counts as an “Opus 5.5 video”

Claude Opus 5.5 (`claude-opus-5-5`, released 2026-09-22) has text + image input and **text output only**.
A qualifying video is one the creator says was made with Opus 5.5 by one of these routes:

1. **Code-drawn** — Opus writes JS/Canvas/WebGL/p5.js/Three.js/HyperFrames/Remotion/Manim code; frames rendered headlessly + ffmpeg
2. **Blender / 3D** — Opus drives Blender (Python, Blender MCP) or a real-time 3D scene and renders camera moves
3. **Director** — Opus writes the shot list / prompts and calls video or image models (Seedance, Kling, Veo, GPT Image …) via MCP or API
4. **Edit / transform** — Opus edits or re-animates supplied footage (talking head → animation, take selection …)

Interactive apps and games count only if the post is primarily a *video* (trailer, film, recorded sequence), not a UI walkthrough.

## Qualification rules

- **Verifiable source**: an X status URL, creator GitHub repo, or official Anthropic page. Fetch it yourself (fxtwitter) — never rely on an aggregator alone.
- **Explicit Opus 5.5 claim** by the creator in the post/thread (not just “Claude”; Opus 5 / 4.x / Fable / Mythos do not count).
- **Media**: the post has a video (or a public repo that renders one). Photos-only → watchlist.
- **Prompts are verbatim only.** Copy from the creator’s post/reply/README with `scripts/extract_prompts.py` cut rules. If no prompt text is public, use `"type": "not_shared"`. Never paraphrase, translate-in-place, “reconstruct”, or summarize a prompt as if it were the prompt. Author descriptions go in `author_description`; long prompts may be `excerpt` with an explicit truncation marker.
- **No fabricated metrics.** Time/cost/token numbers only as “author reports …”.
- **Engagement floor** (soft): prefer ≥ ~50 likes or ≥ ~5k views, unless the prompt/workflow is unusually useful. Below that → watchlist.
- **Dedupe** against every `status/<id>` already in `data/entries.json` and prior `proposals/*/candidates.json`. The same creator can have multiple entries if the videos differ.
- **Rights**: preview still + ≤10 MB compressed clip of the creator’s own post only; no re-upload of full-length originals; honor removal requests (RIGHTS.md).

## Sources and queries (run in this order)

1. **X search** (via WebSearch / unroll mirrors; X search itself needs login). Queries:
   - `"Opus 5.5" video`, `"Opus 5.5" animation`, `"Opus 5.5" "one prompt" OR "one shot" video`
   - `"Opus 5.5" Blender`, `"Opus 5.5" Remotion OR HyperFrames OR Manim OR p5.js OR three.js`
   - `"Opus 5.5" music video`, `"Opus 5.5" explainer`, `"Opus 5.5" Seedance OR Kling OR Veo`
   - Chinese / Japanese: `Opus 5.5 动画 提示词`, `Opus 5.5 视频 prompt`, `Opus 5.5 アニメーション プロンプト`
2. **fxtwitter API** for every candidate (works from the box via curl):
   - Post: `https://api.fxtwitter.com/<user>/status/<id>` → text, author, created_at, likes/views, video URLs + thumbnails
   - Thread + replies (where “prompt below 👇” lives): `https://api.fxtwitter.com/2/conversation/<id>` → keep replies whose author == post author
3. **Official**: [@claudeai](https://x.com/claudeai) launch/explorations threads, [anthropic.com/claude-opus-5-5](https://www.anthropic.com/claude-opus-5-5), claude.com/blog.
4. **Aggregators for discovery only** (always re-verify at the source):
   - [athemeroy/awesome-opus-5-5-videos](https://github.com/athemeroy/awesome-opus-5-5-videos) — `data/cases.csv` (152 reviewed cases, “Prompt shown” label)
   - favtutor.com, go.tabbit.ai/model/claude-opus-5-5/prompts, bittide.aicompass.dev, unrollnow.com, runtimewire.com
5. **GitHub search**: `opus 5.5 video created:>=<yesterday>` (repos like PDoomVideo, functional-emotions-video, shipvideo, opus-js-animations, riso-windowseat).
6. **Reddit** r/ClaudeAI, r/singularity — reddit.com blocks the box (network policy); use secondary mirrors (tabbit, bittide) to discover, then only list if the creator also has an X post/GitHub repo you can fetch, or list the Reddit URL as source with “prompt quoted by <mirror>” in notes → currently watchlist.

## Daily procedure

```bash
D=$(date +%F); P=proposals/$D; mkdir -p $P/{raw,previews,videos,featured,snippets}
# 1) discover → save raw fx JSON:  curl -s https://api.fxtwitter.com/<user>/status/<id> > $P/raw/fx-<id>.json
#                                  curl -s https://api.fxtwitter.com/2/conversation/<id> > $P/raw/conv-<id>.json
# 2) for each qualified candidate: add an object to $P/candidates.json (same schema as data/entries.json)
# 3) media (writes assets into $P/, source into $P/raw/):
python3 scripts/fetch_x_media.py <post_url> <slug> --out $P
# 4) snippets: append README blocks to $P/snippets/README-entries.md and TOC lines to $P/snippets/TOC-bullets.md
# 5) write $P/CHANGELOG.md: new_count, proposed adds, sources checked, skipped/watchlist with reasons
```

On owner approval: merge `candidates.json` objects into `data/entries.json`, copy `$P/previews/*` → `assets/previews/`,
`$P/videos/*` → `assets/videos/`, run `python3 scripts/extract_prompts.py $P/raw && python3 scripts/build_readme.py`, commit.

## Entry schema (`data/entries.json`)

```json
{"slug":"handle-short-title","cat":"films|pixel|music|explainers|blender|director",
 "title":"…","title_zh":"…","handle":"x_handle","name":"Display Name",
 "post":"https://x.com/<handle>/status/<id>","links":[["Code","https://github.com/…"]],
 "desc":"what it is + what the author reports","desc_zh":"…",
 "prompt":{"type":"verbatim|excerpt|author_description|repo_quotes|not_shared",
           "status":"<id of the post/reply holding the prompt>","conv":"<root id>",
           "start_after":"text right before the prompt","end_before":"text right after (optional)","lang":"ja|zh (optional)"}}
```
