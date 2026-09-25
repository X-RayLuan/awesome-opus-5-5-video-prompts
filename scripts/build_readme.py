#!/usr/bin/env python3
"""Render README.md and README.zh-CN.md from data/entries.json + data/prompts/*.txt.
Run after adding entries (see SCRAPE.md). Do not hand-edit generated entry blocks."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "X-RayLuan/awesome-opus-5-5-video-prompts"
CAMPAIGN = "awesome_opus55_video_prompts"
CDN = f"https://cdn.jsdelivr.net/gh/{REPO}@main/assets/videos"

def ev(content):
    return f"https://easyveo.com?utm_source=github&utm_medium=referral&utm_campaign={CAMPAIGN}&utm_content={content}"

CATS = [
    ("films", "🎬 Code-drawn films & shorts", "🎬 代码绘制的短片与动画",
     "Opus 5.5 writes the whole film as JavaScript / Canvas / WebGL (often with Web Audio sound), then renders frames headlessly and muxes with ffmpeg.",
     "Opus 5.5 把整部片子写成 JavaScript / Canvas / WebGL 代码（常用 Web Audio 合成声音），再无头渲染逐帧并用 ffmpeg 合成。"),
    ("pixel", "👾 Pixel-art animation", "👾 像素动画",
     "Tight technical specs (logical resolution, palette, state machine, zero-allocation loop) produce crisp 16-bit-style loops.",
     "用严格的技术规格（逻辑分辨率、调色板、状态机、零分配循环）得到清晰的 16-bit 风格循环动画。"),
    ("music", "🎵 Music videos", "🎵 音乐 MV",
     "Feed a song + lyrics; Opus storyboards, briefs parallel subagents per chapter and beat-syncs every cut.",
     "提供歌曲与歌词；Opus 先写分镜，再按章节分派并行子代理，并让每个剪辑点踩在节拍上。"),
    ("explainers", "📊 Explainers, ads & motion graphics", "📊 讲解、广告与动效",
     "Launch videos, recipe explainers, split-screen lessons and talking-head B-roll — the “instructional video” use case.",
     "发布视频、配方讲解、分屏课程、口播配 B-roll —— 即“讲解型视频”场景。"),
    ("blender", "🧊 Blender & 3D renders", "🧊 Blender 与 3D 渲染",
     "Opus drives Blender (Python / Blender MCP) or real-time 3D to build scenes procedurally and render camera moves.",
     "Opus 通过 Blender Python / Blender MCP 或实时 3D 程序化搭建场景并渲染运镜。"),
    ("director", "🎥 Opus as director for AI video models", "🎥 Opus 当导演：驱动 AI 视频模型",
     "Opus writes character sheets, start frames and shot-by-shot prompts, then calls Seedance / Kling / image models via MCP. This is the lane EasyVeo is built for.",
     "Opus 撰写角色设定、首帧和逐镜提示词，再通过 MCP 调用 Seedance / Kling / 图像模型 —— 这正是 EasyVeo 所服务的场景。"),
]
FEATURED = ["notinreality-pdoom-music-video", "kevin-ngo-what-do-you-love", "lcslates-glass-mosaic-film", "majid-pixel-wizard"]

L = {
 "en": dict(
   h1="# Awesome Opus 5.5 Video Prompts",
   tagline="**A starting point for your next Claude Opus 5.5 video — or your next AI video ad remake.**",
   what=("Claude Opus 5.5 ([Anthropic, Sep 22 2026](https://www.anthropic.com/claude-opus-5-5)) outputs text, not pixels. "
         "The “Opus 5.5 video” wave is the model **writing the film as code** — JavaScript/Canvas/WebGL, p5.js, Blender Python — and rendering it frame by frame with headless Chrome or Blender + ffmpeg, "
         "or **directing video models** like Seedance and Kling. This list collects the best community demos with the prompts their creators actually shared."),
   lede="**{n} examples · {c} categories · EN + ZH · verbatim prompts only · EasyVeo remake lane · CTA: [easyveo.com]({cta})**",
   feat="## Featured projects",
   featsub="<sub>Click a thumb (or ▶ Play) to play the clip in your browser. Clips are compressed; full originals on X.</sub>",
   latest="## Latest Opus 5.5 video prompts", browse="Browse examples",
   play="▶ Play", playv="▶ Play video", orig="Original on X", promptlink="Prompt →",
   prompt_v="**Prompt** · verbatim from the [author’s post]({src})", prompt_lang={"ja": " · original in Japanese", "zh": " · original in Chinese"},
   prompt_x="**Prompt** · excerpt, written by Opus 5.5 and posted in the [author’s thread]({src}) — truncated here; see the thread for every prompt",
   prompt_ns="**Prompt** · _not shared by the author._",
   prompt_ad="**Prompt** · _not shared verbatim._ The author’s description of the direction ([reply]({src})):",
   prompt_rq="**Prompt** · the author’s messages to Claude, as quoted in the [project README]({src})",
   origpost="Original post", remake="Remake with EasyVeo", back="Back to examples", community="community demo", official="official demo",
   ev_title="EasyVeo decode → stills → remake", ev_line="[EasyVeo](https://easyveo.com) · remake the winner, keep your product · EasyVeo workflow (not a community demo)",
   ev_desc="_Use Opus 5.5-style shot planning on a real ad: decode what works, lock product-true stills, then remake with video models._",
   ev_try="Try on EasyVeo",
 ),
 "zh": dict(
   h1="# Awesome Opus 5.5 视频提示词精选",
   tagline="**下一条 Claude Opus 5.5 视频的起点 —— 或下一条 AI 视频广告复刻。**",
   what=("Claude Opus 5.5（[Anthropic，2026 年 9 月 22 日发布](https://www.anthropic.com/claude-opus-5-5)）只输出文本，不直接生成像素。"
         "所谓“Opus 5.5 做视频”，是让模型**把整部片子写成代码** —— JavaScript/Canvas/WebGL、p5.js、Blender Python —— 再用 headless Chrome 或 Blender + ffmpeg 逐帧渲染；"
         "或让它**充当导演驱动 Seedance、Kling 等视频模型**。本列表收录社区最佳演示，只收录作者本人公开的原始提示词。"),
   lede="**{n} 个案例 · {c} 个分类 · 中英双语 · 仅收录原文提示词 · EasyVeo 复刻车道 · CTA：[easyveo.com]({cta})**",
   feat="## 精选项目",
   featsub="<sub>点击缩略图或 ▶ 播放，在浏览器中直接播放。片段已压缩；完整原片在 X。</sub>",
   latest="## 最新 Opus 5.5 视频提示词", browse="浏览全部案例",
   play="▶ 播放", playv="▶ 播放视频", orig="X 原帖", promptlink="提示词 →",
   prompt_v="**提示词** · 原文摘自[作者帖子]({src})", prompt_lang={"ja": " · 原文为日语", "zh": " · 原文为中文"},
   prompt_x="**提示词** · 节选，由 Opus 5.5 撰写、作者发布于[原线程]({src})；此处已截断，完整提示词见原线程",
   prompt_ns="**提示词** · _作者未公开。_",
   prompt_ad="**提示词** · _未公开原文。_ 作者对指令的描述（[回复]({src})）：",
   prompt_rq="**提示词** · 作者发给 Claude 的原话，引自[项目 README]({src})",
   origpost="原帖", remake="用 EasyVeo 复刻", back="返回列表", community="社区演示", official="官方演示",
   ev_title="EasyVeo：拆解 → 分镜静帧 → 复刻", ev_line="[EasyVeo](https://easyveo.com) · 复刻爆款结构，保留你的产品 · EasyVeo 工作流（非社区演示）",
   ev_desc="_把 Opus 5.5 式的分镜规划用在真实广告上：拆解有效结构，锁定产品一致的静帧，再用视频模型复刻。_",
   ev_try="在 EasyVeo 试用",
 ),
}
EV_PROMPT = "Authorized short ad clip (≤30s). Decode hook / pacing / proof / CTA (~18 elements). Produce product-true stills, then a Seedance 2.5 / multi-model remake that keeps my SKU. No invented ROAS."

def load():
    es = json.load(open(os.path.join(ROOT, "data/entries.json")))
    for e in es:
        p = os.path.join(ROOT, "data/prompts", e["slug"] + ".txt")
        e["prompt_text"] = open(p).read().rstrip("\n") if os.path.exists(p) else None
        e["has_video"] = os.path.exists(os.path.join(ROOT, "assets/videos", e["slug"] + "-readme.mp4"))
        e["media"] = MEDIA.get(e["slug"], {})
    return es

MP = os.path.join(ROOT, "data/media.json")
MEDIA = {m["slug"]: m for m in json.load(open(MP))} if os.path.exists(MP) else {}

def status_url(e):
    p = e["prompt"]
    return f"https://x.com/{e['handle']}/status/{p['status']}" if p.get("status") else e["post"]

def fence(txt):
    return "```text\n" + txt + "\n```"

def clip_note(e, lang):
    m = e.get("media") or {}
    if not m.get("trimmed"):
        return ""
    return (f" (前 {int(m['clip_seconds'])} 秒 / 全长 {int(m['src_duration'])} 秒)" if lang == "zh"
            else f" (first {int(m['clip_seconds'])} s of {int(m['src_duration'])} s)")

def snippets(slugs, outdir, lang="en"):
    """Write proposals/<date>/snippets/{README-entries.md,TOC-bullets.md} for the given slugs."""
    es = [e for e in load() if e["slug"] in slugs]
    os.makedirs(os.path.join(outdir, "snippets"), exist_ok=True)
    open(os.path.join(outdir, "snippets/README-entries.md"), "w").write(
        "<!-- Generated by scripts/build_readme.py. Paste under the matching category in README.md (or merge into data/entries.json and rebuild). -->\n\n"
        + "\n".join(entry(e, lang) for e in es))
    open(os.path.join(outdir, "snippets/TOC-bullets.md"), "w").write("\n".join(
        f"- [{e['title']}](#{e['slug']}) · @{e['handle']}" + (" · video" if e["has_video"] else "") for e in es) + "\n")

def entry(e, lang):
    t = L[lang]; title = e["title_zh"] if lang == "zh" else e["title"]
    desc = e["desc_zh"] if lang == "zh" else e["desc"]
    vid = f"{CDN}/{e['slug']}-readme.mp4"; img = f"assets/previews/{e['slug']}.webp"
    kind = t["official"] if e["handle"] == "claudeai" else t["community"]
    out = [f"### {title}", f'<a id="{e["slug"]}"></a>', "",
           f"[@{e['handle']}](https://x.com/{e['handle']}) · {e['name']} · {kind} · Claude Opus 5.5", ""]
    if e["has_video"]:
        out += [f'<a href="{vid}"><img src="{img}" width="640" loading="lazy" alt="Play video"></a><br>',
                f'<sub><a href="{vid}">{t["playv"]}</a>{clip_note(e, lang)} · <a href="{e["post"]}">{t["orig"]}</a></sub>', ""]
    else:
        out += [f'<a href="{e["post"]}"><img src="{img}" width="640" loading="lazy" alt="{title}"></a>', ""]
    out += [f"_{desc}_", ""]
    p = e["prompt"]; src = status_url(e)
    if p["type"] == "verbatim":
        out += [t["prompt_v"].format(src=src) + t["prompt_lang"].get(p.get("lang"), ""), "", fence(e["prompt_text"])]
    elif p["type"] == "excerpt":
        out += [t["prompt_x"].format(src=src), "", fence(e["prompt_text"] + "\n\n[…]")]
    elif p["type"] == "author_description":
        out += [t["prompt_ad"].format(src=src), "", "> " + e["prompt_text"].replace("\n", "\n> ")]
    elif p["type"] == "repo_quotes":
        repo = dict(e["links"]).get("Code", e["post"])
        out += [t["prompt_rq"].format(src=repo), "", fence(e["prompt_text"])]
    else:
        note = p.get("note")
        out += [t["prompt_ns"] + (f" {note}" if note and lang == "en" else "")]
    links = [f"[{t['origpost']}]({e['post']})"] + [f"[{k}]({u})" for k, u in e["links"]]
    links += [f"[{t['remake']}]({ev(e['slug'].replace('-', '_'))})", f"[{t['back']}](#all-prompts)"]
    out += ["", " · ".join(links), "", "---", ""]
    return "\n".join(out)

def featured(es, lang):
    t = L[lang]; by = {e["slug"]: e for e in es}; cells = []
    for s in FEATURED:
        e = by[s]; title = e["title_zh"] if lang == "zh" else e["title"]; vid = f"{CDN}/{s}-readme.mp4"
        cells.append(f'<td width="50%" valign="top"><a href="{vid}"><img src="assets/previews/{s}.webp" width="420" loading="lazy" alt="{title}"></a><br>'
                     f'<strong><a href="#{s}">{title}</a></strong><br><sub><a href="{e["post"]}">@{e["handle"]}</a> · <a href="{vid}">{t["play"]}</a></sub><br>'
                     f'<a href="#{s}">{t["promptlink"]}</a></td>')
    rows = ["<table>"]
    for i in range(0, len(cells), 2):
        rows += ["<tr>", *cells[i:i+2], "</tr>"]
    return "\n".join(rows + ["</table>"])

def toc(es, lang):
    t = L[lang]; out = ["<details>", f"<summary>{t['browse']}</summary>", ""]
    for key, en, zh, *_ in CATS:
        out.append(f"**{zh if lang == 'zh' else en}**")
        for e in [x for x in es if x["cat"] == key]:
            title = e["title_zh"] if lang == "zh" else e["title"]
            tag = " · video" if e["has_video"] else ""
            pr = " · prompt" if e["prompt"]["type"] in ("verbatim", "excerpt", "repo_quotes") else ""
            out.append(f"- [{title}](#{e['slug']}) · @{e['handle']}{tag}{pr}")
        if key == "director":
            out.append(f"- [{t['ev_title']}](#easyveo-remake-loop)")
        out.append("")
    return "\n".join(out + ["</details>"])

def easyveo_entry(lang):
    t = L[lang]
    return "\n".join([f"### {t['ev_title']}", '<a id="easyveo-remake-loop"></a>', "", t["ev_line"], "", t["ev_desc"], "",
                      "**Prompt**" if lang == "en" else "**提示词**", "", fence(EV_PROMPT), "",
                      f"[{t['ev_try']}]({ev('entry_studio')}) · [{t['back']}](#all-prompts)", "", "---", ""])

TAIL = {
"en": """## Tools & starter kits

- [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) — full source of the P(doom) music video: p5.js studio page, `render.mjs` (headless Chrome → ffmpeg), `STORYBOARD.md`, `ANIMATION_GUIDE.md`
- [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) — starter kit for p5.js + p5.brush character animation with Opus 5.5 (“Read ANIMATION_GUIDE.md, then make a 15-second video of …”)
- [ledbetterljoshua/functional-emotions-video](https://github.com/ledbetterljoshua/functional-emotions-video) — custom WebGL2 brushstroke renderer + beat/lyric alignment pipeline
- [klsoen/opus-js-animations](https://github.com/klsoen/opus-js-animations) — Claude Code skill: brief → sound → director’s treatment → frame-exact MP4
- [buildwithhanif/claude-animation-skill](https://github.com/buildwithhanif/claude-animation-skill) — Node Canvas animation skill with character rig and frame checks
- [diggerhq/shipvideo](https://github.com/diggerhq/shipvideo) ([launchvideo.io](https://launchvideo.io)) — URL/prompt → launch video; Opus 5.5 writes one HTML film, rendered under a virtual clock
- [Blender MCP + Opus 5.5 guide](https://blendermcp.org/guides/claude-opus-5-5-blender) — model ID and API changes when driving Blender
- [dev.to: “This video is about how this video was made”](https://dev.to/peter/this-video-is-about-how-this-video-was-made-42hl) — deep dive on the deterministic `renderAt(t)` pattern, ElevenLabs cue timing and reviewer subagents

## Related indexes

- [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) — official announcement · [@claudeai launch thread](https://x.com/claudeai/status/2102471866635919731)
- [athemeroy/awesome-opus-5-5-videos](https://github.com/athemeroy/awesome-opus-5-5-videos) — research-style index of 1,000+ Opus 5.5 video posts with production-path labels
- This list welcomes PRs via [CONTRIBUTING.md](CONTRIBUTING.md)

## Share a good example

Open a PR — see [CONTRIBUTING.md](CONTRIBUTING.md). Only verbatim prompts the creator published; otherwise mark “not shared”. Keep full videos on X.

## Credits

Community demos scraped from public X posts (via the fxtwitter API), creator GitHub repos, and Anthropic’s [@claudeai](https://x.com/claudeai/status/2102471866635919731) launch thread. Layout mirrors [awesome-gpt-6-astra-prompts](https://github.com/X-RayLuan/awesome-gpt-6-astra-prompts). Product CTA: [EasyVeo](https://easyveo.com).

See [RIGHTS.md](RIGHTS.md). Not affiliated with Anthropic.
""",
"zh": """## 工具与模板

- [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) —— P(doom) MV 完整源码：p5.js 画布页、`render.mjs`（headless Chrome → ffmpeg）、`STORYBOARD.md`、`ANIMATION_GUIDE.md`
- [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) —— 用 Opus 5.5 做 p5.js + p5.brush 角色动画的起步模板
- [ledbetterljoshua/functional-emotions-video](https://github.com/ledbetterljoshua/functional-emotions-video) —— 自研 WebGL2 笔触渲染器 + 节拍/歌词对齐流程
- [klsoen/opus-js-animations](https://github.com/klsoen/opus-js-animations) —— Claude Code 技能：需求 → 声音 → 导演方案 → 逐帧精确 MP4
- [buildwithhanif/claude-animation-skill](https://github.com/buildwithhanif/claude-animation-skill) —— Node Canvas 动画技能，含角色骨骼与逐帧检查
- [diggerhq/shipvideo](https://github.com/diggerhq/shipvideo)（[launchvideo.io](https://launchvideo.io)）—— 输入 URL/提示词生成发布视频；Opus 5.5 写单个 HTML 影片，虚拟时钟逐帧渲染
- [Blender MCP + Opus 5.5 指南](https://blendermcp.org/guides/claude-opus-5-5-blender) —— 驱动 Blender 时的模型 ID 与 API 变化
- [dev.to：《This video is about how this video was made》](https://dev.to/peter/this-video-is-about-how-this-video-was-made-42hl) —— 详解确定性 `renderAt(t)` 渲染、ElevenLabs 提示词时间轴与评审子代理

## 相关索引

- [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5) —— 官方发布 · [@claudeai 发布串](https://x.com/claudeai/status/2102471866635919731)
- [athemeroy/awesome-opus-5-5-videos](https://github.com/athemeroy/awesome-opus-5-5-videos) —— 研究型索引，覆盖 1,000+ 条 Opus 5.5 视频帖并标注制作路径
- 欢迎通过 [CONTRIBUTING.md](CONTRIBUTING.md) 提交 PR

## 分享好案例

提交 PR —— 见 [CONTRIBUTING.md](CONTRIBUTING.md)。只收录作者本人公开的提示词原文，否则标注“未公开”。完整视频请保留在 X。

## 致谢

社区演示整理自公开 X 帖子（通过 fxtwitter API）、作者 GitHub 仓库，以及 Anthropic [@claudeai](https://x.com/claudeai/status/2102471866635919731) 发布串。版式沿用 [awesome-gpt-6-astra-prompts](https://github.com/X-RayLuan/awesome-gpt-6-astra-prompts)。Product CTA: [EasyVeo](https://easyveo.com)。

见 [RIGHTS.md](RIGHTS.md)。与 Anthropic 无关联。
"""}

def build(lang):
    es = load(); t = L[lang]; zh = lang == "zh"; pre = "zh_" if zh else ""
    badges = (f"[![Awesome](https://awesome.re/badge-flat2.svg)](https://github.com/sindresorhus/awesome) "
              f"[![GitHub stars](https://img.shields.io/github/stars/{REPO}?style=flat-square&color=f5c542)](https://github.com/{REPO}/stargazers) "
              f"[![License: MIT](https://img.shields.io/badge/License-MIT-64748b?style=flat-square)](LICENSE) "
              f"[![Try EasyVeo](https://img.shields.io/badge/Try-EasyVeo-0ea5e9?style=flat-square)]({ev(pre + 'badge')}) "
              f"[![Contributions welcome](https://img.shields.io/badge/PRs-welcome-238636?style=flat-square)](CONTRIBUTING.md)")
    en_b = "English-✓-238636" if not zh else "English-64748b"
    zh_b = "%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-✓-238636" if zh else "%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-64748b"
    hero = ev(pre + "readme_hero").replace("&", "&amp;")
    parts = [t["h1"], "", badges, "", "<p>",
             f'  <a href="README.md"><img alt="English" src="https://img.shields.io/badge/{en_b}?style=flat-square"></a>',
             f'  <a href="README.zh-CN.md"><img alt="简体中文" src="https://img.shields.io/badge/{zh_b}?style=flat-square"></a>',
             "</p>", "", f'<a href="{hero}"><img src="assets/hero.webp" width="100%" alt="Awesome Opus 5.5 Video Prompts"></a>', "",
             t["tagline"], "", t["what"], "", t["lede"].format(n=len(es), c=len(CATS), cta=ev(pre + "lede")), "",
             t["feat"], "", t["featsub"], "", featured(es, lang), "", '<a id="all-prompts"></a>', "", t["latest"], "", toc(es, lang), "", "---", ""]
    for key, en, zhn, den, dzh in CATS:
        parts += [f"## {zhn if zh else en}", "", f"_{dzh if zh else den}_", ""]
        for e in [x for x in es if x["cat"] == key]:
            parts.append(entry(e, lang))
        if key == "director":
            parts.append(easyveo_entry(lang))
    parts.append(TAIL[lang])
    fn = "README.zh-CN.md" if zh else "README.md"
    open(os.path.join(ROOT, fn), "w").write("\n".join(parts))
    print("wrote", fn, len(es), "entries")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--snippets":   # --snippets proposals/<date> slug1 slug2 ... (or 'all')
        slugs = sys.argv[3:] if sys.argv[3:] != ["all"] else [e["slug"] for e in load()]
        snippets(set(slugs), sys.argv[2])
    else:
        build("en"); build("zh")
