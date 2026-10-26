"""Maria's own clips: turns a raw phone video into a finished, branded reel.

How it's used
  Drop a vertical phone video (mp4 / mov) into clips/inbox/ on GitHub. The next reel
  slot uses the oldest clip there instead of a reel from the content bank. After it
  posts, the clip moves to clips/used/ so it never posts twice.

  Optional: add a .txt file with the same name (my-clip.mp4 + my-clip.txt) to write
  the caption yourself. Without it, the caption is what you said in the clip.

What the bot adds
  - Fills the 9:16 frame (crops sideways videos to fit)
  - Burned-in subtitles, timed word by word (speech recognition with faster-whisper)
  - IMADI Tech logo and "Maria Aziz · Founder" at the top, WhatsApp number at the bottom
  - A closing call-to-action scene
  - Even loudness, so every reel sounds the same

For offline tests, FAKE_SUBS=1 skips speech recognition and uses sample subtitles.
"""
import html
import json
import os
import re
import subprocess
from pathlib import Path

from . import config, render
from .reel import FADE, FPS, _duration, _run, _still_clip

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "clips" / "inbox"
USED = ROOT / "clips" / "used"
VIDEO_EXT = {".mp4", ".mov", ".m4v"}
CTA_SECONDS = 2.8


def next_clip() -> Path | None:
    clips = sorted(p for p in INBOX.glob("*") if p.suffix.lower() in VIDEO_EXT)
    return clips[0] if clips else None


# ---------------------------------------------------------------- speech --
def transcribe(video: Path) -> list[tuple[float, float, str]]:
    """Word timings [(start, end, word)]. Empty list if speech recognition isn't available."""
    if os.environ.get("FAKE_SUBS") == "1":
        sample = "Most businesses lose leads at night because nobody replies. So I built a bot that answers in seconds".split()
        return [(0.3 + i * 0.32, 0.3 + i * 0.32 + 0.3, w) for i, w in enumerate(sample)]
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("small.en", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(video), language="en", word_timestamps=True, vad_filter=True)
        return [(w.start, w.end, w.word.strip()) for seg in segments for w in (seg.words or []) if w.word.strip()]
    except Exception as e:  # never block a post because of subtitles
        print("Subtitles skipped:", e)
        return []


def _chunks(words, max_words=3, max_gap=0.45):
    """Groups words into short on-screen lines (2-3 words, the style that reads well on reels)."""
    out, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w[0] - cur[-1][1] > max_gap or re.search(r"[.!?,]$", cur[-1][2])):
            out.append(cur)
            cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    return [(c[0][0], max(c[-1][1], c[0][0] + 0.35), " ".join(x[2] for x in c)) for c in out]


def _ts(t: float) -> str:
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def write_ass(words, path: Path) -> Path | None:
    if not words:
        return None
    lines = []
    for start, end, text in _chunks(words):
        text = re.sub(r"[{}\\]", "", text).upper()
        lines.append(f"Dialogue: 0,{_ts(start)},{_ts(end)},Sub,,0,0,0,,{text}")
    path.write_text(
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, "
        "StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        # White text, near-black outline and soft shadow; bottom-center, above the WhatsApp bar.
        "Style: Sub,Inter ExtraBold,78,&H00FFFFFF,&H00FFFFFF,&H00180F0A,&H64000000,-1,0,0,0,100,100,0,0,1,7,3,2,80,80,430,1\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n" + "\n".join(lines) + "\n",
        encoding="utf-8")
    return path


def caption_for(video: Path, words) -> str:
    side = video.with_suffix(".txt")
    if side.exists() and side.read_text(encoding="utf-8").strip():
        return side.read_text(encoding="utf-8").strip()
    said = " ".join(w[2] for w in words).strip()
    said = re.sub(r"\s+([,.!?])", r"\1", said)
    if said:
        return f"{said}\n\nMaria Aziz, founder of IMADI Tech."
    return "A quick note from Maria Aziz, founder of IMADI Tech."


# --------------------------------------------------------------- overlay --
def overlay_html() -> str:
    """Transparent 1080x1920 layer: brand at the top, WhatsApp at the bottom, soft shading for legibility."""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;background:transparent;overflow:hidden;font-family:Inter,Arial,sans-serif;color:#fff}}
.shade-top{{position:absolute;left:0;right:0;top:0;height:300px;background:linear-gradient(rgba(6,10,28,.62),rgba(6,10,28,0))}}
.shade-bot{{position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(rgba(6,10,28,0),rgba(6,10,28,.7))}}
.top{{position:absolute;top:70px;left:64px;right:64px;display:flex;align-items:center;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:800;font-size:34px;letter-spacing:.5px}}
.brand img{{height:50px}}.brand span{{font-weight:300;letter-spacing:6px;font-size:26px;margin-left:4px;opacity:.9}}
.who{{font-size:24px;font-weight:600;letter-spacing:1px;background:rgba(10,15,36,.55);border:2px solid rgba(255,255,255,.35);padding:10px 22px;border-radius:40px}}
.wa{{position:absolute;left:50%;bottom:110px;transform:translateX(-50%);display:flex;align-items:center;gap:16px;font-size:34px;font-weight:800;
  background:#25d366;color:#04210f;padding:18px 36px;border-radius:60px;white-space:nowrap}}
.wa i{{width:46px;height:46px;border-radius:50%;background:#04210f;display:grid;place-items:center}}
</style></head><body>
<div class="shade-top"></div><div class="shade-bot"></div>
<div class="top"><div class="brand"><img src="{render.LOGO}" alt="">IMADI<span>TECH</span></div><div class="who">Maria Aziz · Founder</div></div>
<div class="wa"><i>{render.WA_ICON.replace('width="32" height="32"', 'width="28" height="28"')}</i>WhatsApp {html.escape(config.WHATSAPP_DISPLAY)}</div>
</body></html>"""


# ----------------------------------------------------------------- build --
def build(video: Path, theme: str, out_dir: Path) -> tuple[Path, str]:
    """Returns (reel.mp4, caption)."""
    work = out_dir / "_clip"
    work.mkdir(parents=True, exist_ok=True)

    words = transcribe(video)
    ass = write_ass(words, work / "subs.ass")
    overlay, cta = render.render([(overlay_html(), 1080, 1920)], work, "overlay", transparent=True) + \
        render.render([(render.scene_html({"headline": "Want this for *your business?*", "sub": "Message IMADI Tech on WhatsApp."},
                                          theme, last=True, tag="IMADI Tech"), 1080, 1920)], work, "cta")

    has_audio = bool(_run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(video)]))
    length = _duration(video)

    # 1) Fill 9:16, add the overlay and subtitles, even out loudness.
    vf = (f"[0:v]fps={FPS},scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[base];"
          f"[base][1:v]overlay=0:0,format=yuv420p")
    if ass:
        fonts = (ROOT / "assets" / "fonts").as_posix()
        vf += f",subtitles='{ass.as_posix()}':fontsdir='{fonts}'"
    vf += "[v]"
    main = work / "main.mp4"
    args = ["ffmpeg", "-y", "-i", str(video), "-loop", "1", "-i", str(overlay)]
    if not has_audio:
        args += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    args += ["-filter_complex", vf + (";[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" if has_audio else ""),
             "-map", "[v]", "-map", "[a]" if has_audio else "2:a", "-t", f"{length:.3f}",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-r", str(FPS), "-c:a", "aac", "-b:a", "160k", "-ar", "48000", str(main)]
    _run(args)

    # 2) Closing scene, crossfaded in; the clip's audio fades out under it.
    cta_clip = _still_clip(cta, CTA_SECONDS, work / "cta.mp4")
    off = max(length - FADE, 0.1)
    out = out_dir / "reel.mp4"
    _run(["ffmpeg", "-y", "-i", str(main), "-i", str(cta_clip), "-f", "lavfi", "-t", f"{CTA_SECONDS:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
          "-filter_complex",
          f"[0:v][1:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v];"
          f"[0:a]afade=t=out:st={max(length - 0.6, 0):.3f}:d=0.6[a0];[a0][2:a]concat=n=2:v=0:a=1[a]",
          "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)])
    (work / "words.json").write_text(json.dumps(words), encoding="utf-8")
    return out, caption_for(video, words)


def mark_used(video: Path) -> None:
    """Moves the clip (and its caption file) to clips/used/ and pushes, so it never posts twice."""
    USED.mkdir(parents=True, exist_ok=True)
    moved = [video] + ([video.with_suffix(".txt")] if video.with_suffix(".txt").exists() else [])
    def git(*a):
        subprocess.run(["git", *a], cwd=ROOT, check=True, capture_output=True, text=True)
    git("config", "user.name", "IMADI Marketing Bot")
    git("config", "user.email", "bot@imadi.tech")
    for f in moved:
        git("mv", str(f.relative_to(ROOT)), str((USED / f.name).relative_to(ROOT)))
    git("commit", "-m", f"Posted clip {video.name}")
    for attempt in range(3):
        try:
            git("pull", "--rebase", "-q")
            git("push", "-q")
            return
        except subprocess.CalledProcessError:
            if attempt == 2:
                raise
