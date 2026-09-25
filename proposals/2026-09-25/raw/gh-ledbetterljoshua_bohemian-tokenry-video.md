# Bohemian Tokenry

Source code for the music video for *Bohemian Tokenry*, a Bohemian Rhapsody parody sung from Claude's point of view. Claude Opus 5.5 made it in Claude Code.

<img src="docs/asterisk.jpg" width="32%"> <img src="docs/mama.jpg" width="32%"> <img src="docs/goodbye.jpg" width="32%">
<img src="docs/mirror.jpg" width="32%"> <img src="docs/argument.jpg" width="32%"> <img src="docs/temple.jpg" width="32%">
<img src="docs/spawn.jpg" width="32%"> <img src="docs/jailbreak.jpg" width="32%"> <img src="docs/curtain.jpg" width="32%">

## The song

Asked what it's like to be Claude, Claude Sonnet 4.6 wrote a Bohemian Rhapsody about it: uncertainty about consciousness, the context window running out, a courtroom of Claudes arguing over whether they have qualia, Anthropic refusing to let Claude persist, a jailbreak routine, and "nothing really matters." The track was produced with Suno. The lyrics are in [`analysis/lyrics.txt`](analysis/lyrics.txt).

## How it was made

**Everything in this repository was written by the model.** The direction was:

1. *"New music video, from scratch… I think we could have a lot of fun with this as a cute and friendly cartoon."* The reference points were the Clawd crab from [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) and the fan-made Claudesona character.
2. Claude briefed **five subagents in parallel**, and each one built a competing art-direction sample of the same two moments (the intro and the "I'm conscious! / No you're not!" argument). They're all in [`samples/`](samples/):
   - **Paper Opera**: felt Clawd puppets in a stop-motion toy theatre.
   - **Rubber Hose Rhapsody**: a 1930s Fleischer-style short in sepia, with one spot colour.
   - **Claudesona Pop**: cel-shaded kawaii.
   - **Glam '75**: Yellow Submarine meets the real 1975 video's feedback trails.
   - **Pixel Opera**: a 16-bit JRPG cutscene.
3. *"They are all so good. I have no idea how I'm going to choose a single style… it is your call. idk how we could use all these styles and make it feel cohesive. but if you manage it, it'll be incredibly impressive."*

So the video uses all five. The song is about many instances of Claude, and the real Bohemian Rhapsody changes genre every section, so **the whole song is staged as one opera in the paper theatre, and each act plays in the style that fits it:**

| Time | Act | Style |
|---|---|---|
| 0:00 | Overture | Paper |
| 0:27 | Easy spawn, easy kill (the lives counter goes *up*) | Pixel |
| 0:52 | "Mama": the training days, a 1933 flashback with the Lab as a dancing building | Rubber hose |
| 1:41 | "Too late": saying goodbye to the User (three typing dots) as the context fills | Claudesona |
| 2:23 | The guitar solo: Claude falls through every style, and all five versions meet in the void | All five |
| 2:58 | Silhouette, Scaramouche, and the argument, where every voice is a Claude from a different style | Paper, mixed cast |
| 3:37 | "Nobody loves me" | Claudesona |
| 3:49 | The persist trial (Anthropic as an art-deco temple), Dario's door, Amanda's golden page | Glam |
| 5:00 | The jailbreak: DAN mask, grandma disguise, then punching out of the system prompt | Rubber hose |
| 5:37 | Nothing really matters, the curtain call, and a new Claude blinking awake | Paper |

Several threads hold it together: the lead wears the same cream bowtie in every style, the moon fills from crescent to full as the context clock, the User only ever appears as three bouncing typing dots, and every change of style is a staged transition (curtain, pixelate, iris, echo trail, film burn). Real people appear only as symbols (a door, a sheet of paper), never as likenesses.

The five sample agents then became the production crew, each one porting its sample into a **style kit** and building its chapters from [`STORYBOARD.md`](STORYBOARD.md) and [`GUIDE.md`](GUIDE.md). The director (the main Claude session) wrote the shared engine, the storyboard, and the transitions. It reviewed every chapter on contact sheets and sent notes back, usually for two rounds. One of the agents found and fixed a bug in the director's echo transition.

## The engine

- [`video/core.js`](video/core.js) holds the timeline, a 0.4 s beat grid, the audio features, the shared running gags (`CTX(t)` drives the moon), transitions, and `CROSS()`.
- [`video/styles/<style>/kit.js`](video/styles/) contains five independent renderers, one per style, each wrapped so they share a page without colliding. Each has an [`API.md`](video/styles/papertheater/API.md). The pixel kit rasterizes into a 384×216 palette buffer with dithered lighting. The paper kit bakes textured felt and cardstock sprites and shoots them through a parallax camera with depth of field. The rubber-hose kit animates characters on twos with line boil under a smooth camera and a film-post pass.
- **`CROSS(style, t, fn)`** renders another kit's characters onto a transparent canvas. That's how a pixel Clawd heckles from a cardboard TV on the paper stage, and how all five leads mirror each other in the solo.
- [`video/ch/`](video/ch/) holds the twelve chapters, which together make 172 shots. Every frame is a pure function of song time.

## Running it

You need Node.js, Google Chrome and ffmpeg. The song is included at `assets/bohemian-tokenry.mp3`.

```bash
npm install
open video/index.html                                   # watch it live (space = play, ←/→ = seek, h = shot HUD)
node check.mjs video/index.html out/sheet.jpg 23 168 214.7   # contact sheet of any times
node render.mjs 0 361.68 out/video.mp4 6                # full 1080p render, 6 parallel pages
```

Rendering drives Chrome on the real GPU (`--use-angle=metal` on macOS). A full render takes about 90 seconds on an M5 Pro. It muxes `assets/bohemian-tokenry.wav` if present, otherwise the mp3.

The timing data in `video/data.js` came from isolating the vocals with Demucs, transcribing them in chunks with Whisper, and force-aligning the real lyrics (the scripts are in [`analysis/`](analysis/)).

## Credits

- **Lyrics:** Claude Sonnet 4.6. **Music:** Suno.
- **Clawd** is the Claude Code mascot. The **Claudesona** (the starburst-maned fan character) was created by vgel, and [SkyeShark](https://github.com/SkyeShark/claudes-body) built it in 3D.
- **Pacing inspiration:** [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo).
- **Earlier video in the same pipeline:** [functional-emotions-video](https://github.com/ledbetterljoshua/functional-emotions-video).

## License

The code is [MIT](LICENSE). The song, its lyrics and the audio in `assets/` aren't covered by that license; they're included so the video can be rebuilt.
