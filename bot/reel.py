"""Builds a finished 9:16 reel: rendered scenes joined with crossfades,
and an American English voiceover timed so each line plays over its own scene.

Voiceover uses edge-tts (Microsoft's free neural voices, no API key). For offline
tests set FAKE_TTS=1 to use silent placeholder audio instead.
"""
import asyncio
import os
import subprocess
from pathlib import Path

from . import render

FADE = 0.4          # crossfade between scenes, seconds
GAP = 0.45          # pause after each voiceover line
TAIL = 1.6          # hold on the last scene after the final line
FPS = 30


def _run(args: list[str]) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def _duration(path: Path) -> float:
    return float(_run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                       "-of", "default=noprint_wrappers=1:nokey=1", str(path)]))


async def _tts(text: str, voice: str, out: Path) -> None:
    import edge_tts
    await edge_tts.Communicate(text, voice, rate="+4%").save(str(out))


def synthesize(lines: list[str], voice: str, work: Path) -> list[Path]:
    paths = []
    for i, line in enumerate(lines, start=1):
        out = work / f"vo-{i}.mp3"
        if os.environ.get("FAKE_TTS") == "1":
            secs = max(1.2, len(line.split()) / 2.6)  # roughly natural speaking pace
            _run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{secs:.2f}", "-q:a", "9", str(out)])
        else:
            for attempt in range(3):
                try:
                    asyncio.run(_tts(line, voice, out))
                    break
                except Exception:
                    if attempt == 2:
                        raise
        paths.append(out)
    return paths


def _voice_track(clips: list[Path], pads: list[float], out: Path) -> None:
    """Joins voiceover clips, adding pads[i] seconds of silence after clip i."""
    parts, filters = [], []
    for i, (c, pad) in enumerate(zip(clips, pads)):
        parts += ["-i", str(c)]
        filters.append(f"[{i}:a]aresample=44100,apad=pad_dur={max(pad, 0):.3f}[a{i}]")
    n = len(clips)
    concat = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[aout]"
    _run(["ffmpeg", "-y", *parts, "-filter_complex", ";".join(filters + [concat]), "-map", "[aout]", "-c:a", "aac", "-b:a", "160k", str(out)])


def _still_clip(png: Path, seconds: float, out: Path) -> Path:
    _run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-t", f"{seconds:.3f}",
          "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
          "-tune", "stillimage", "-r", str(FPS), str(out)])
    return out


def _join(vids: list[Path], durs: list[float], audio: Path, out: Path) -> Path:
    """Crossfades the clips together and adds the voiceover track."""
    inputs, chain, offset, prev = [], [], 0.0, "[0:v]"
    for v in vids:
        inputs += ["-i", str(v)]
    for i in range(1, len(vids)):
        offset += durs[i - 1] - FADE
        label = f"[v{i}]"
        chain.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={offset:.3f}{label}")
        prev = label
    args = ["ffmpeg", "-y", *inputs, "-i", str(audio)]
    if chain:
        args += ["-filter_complex", ";".join(chain)]
    args += ["-map", prev if chain else "0:v", "-map", f"{len(vids)}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)]
    _run(args)
    return out


def build(item: dict, theme: str, voice: str, out_dir: Path) -> Path:
    """Talking reel: text scenes, one voiceover line per scene."""
    scenes, lines = item["scenes"], item["voiceover"]
    if len(scenes) != len(lines):
        raise ValueError("Each reel scene needs exactly one voiceover line.")
    work = out_dir / "_reel"
    work.mkdir(parents=True, exist_ok=True)

    clips = synthesize(lines, voice, work)
    lens = [_duration(c) for c in clips]
    n = len(scenes)
    durs = [lens[i] + GAP + FADE for i in range(n - 1)] + [lens[-1] + TAIL]
    audio = work / "voice.m4a"
    _voice_track(clips, [GAP] * (n - 1) + [TAIL], audio)

    # The logo, tag and footer sit in the same place on every scene, so only the
    # message changes on screen as the scenes crossfade.
    pages = [(render.scene_html(s, theme, last=(i == n - 1)), 1080, 1920) for i, s in enumerate(scenes)]
    pngs = render.render(pages, work, "scene")
    vids = [_still_clip(png, d, work / f"scene-{i + 1}.mp4") for i, (png, d) in enumerate(zip(pngs, durs))]
    return _join(vids, durs, audio, out_dir / "reel.mp4")


def build_demo(item: dict, theme: str, voice: str, out_dir: Path) -> Path:
    """Client demo reel: the real screen recording inside a branded 9:16 frame with
    narration, then a closing call-to-action scene."""
    work = out_dir / "_reel"
    work.mkdir(parents=True, exist_ok=True)
    video = render.ROOT / "assets" / "demos" / item["video"]

    lines = item["narration"] + [item["cta"]["line"]]
    clips = synthesize(lines, voice, work)
    lens = [_duration(c) for c in clips]
    talk = sum(lens[:-1]) + GAP * (len(lens) - 2)
    shown = max(_duration(video), talk + 0.6)       # demo stays on screen at least this long
    durs = [shown + FADE, lens[-1] + TAIL]
    pads = [GAP] * (len(lens) - 2) + [shown - talk, TAIL]
    audio = work / "voice.m4a"
    _voice_track(clips, pads, audio)

    frame, cta = render.render([
        (render.demo_frame_html(item, theme), 1080, 1920),
        (render.scene_html({"headline": item["cta"]["headline"], "sub": "Chat with IMADI Tech on WhatsApp."}, theme, last=True), 1080, 1920),
    ], work, "demo")

    # Fit the recording inside the card, keeping its shape, centered.
    bx, by, bw, bh = render.DEMO_VIDEO_BOX
    vw, vh = (int(v) for v in _run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                     "stream=width,height", "-of", "csv=p=0", str(video)]).split(","))
    scale = min(bw / vw, bh / vh)
    w, h = int(vw * scale) // 2 * 2, int(vh * scale) // 2 * 2
    x, y = bx + (bw - w) // 2, by + (bh - h) // 2
    demo_clip = work / "demo.mp4"
    _run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(frame), "-i", str(video),
          "-filter_complex",
          f"[1:v]fps={FPS},scale={w}:{h}:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=120[d];"
          f"[0:v][d]overlay={x}:{y}:shortest=0,format=yuv420p[v]",
          "-map", "[v]", "-t", f"{durs[0]:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", str(FPS), str(demo_clip)])
    cta_clip = _still_clip(cta, durs[1], work / "cta.mp4")
    return _join([demo_clip, cta_clip], durs, audio, out_dir / "reel.mp4")
