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


def build(item: dict, theme: str, voice: str, out_dir: Path) -> Path:
    scenes, lines = item["scenes"], item["voiceover"]
    if len(scenes) != len(lines):
        raise ValueError("Each reel scene needs exactly one voiceover line.")
    work = out_dir / "_reel"
    work.mkdir(parents=True, exist_ok=True)

    # 1. Voiceover, one clip per scene.
    clips = synthesize(lines, voice, work)
    lens = [_duration(c) for c in clips]
    n = len(scenes)
    durs = [lens[i] + GAP + FADE for i in range(n - 1)] + [lens[-1] + TAIL]

    # 2. Audio track: each line followed by silence so it lines up with its scene.
    parts, filters = [], []
    for i, c in enumerate(clips):
        parts += ["-i", str(c)]
        pad = (durs[i] - FADE - lens[i]) if i < n - 1 else (durs[i] - lens[i])
        filters.append(f"[{i}:a]aresample=44100,apad=pad_dur={pad:.3f}[a{i}]")
    concat = "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[aout]"
    audio = work / "voice.m4a"
    _run(["ffmpeg", "-y", *parts, "-filter_complex", ";".join(filters + [concat]), "-map", "[aout]", "-c:a", "aac", "-b:a", "160k", str(audio)])

    # 3. Scene images.
    pages = [(render.scene_html(s, theme, last=(i == n - 1)), 1080, 1920) for i, s in enumerate(scenes)]
    pngs = render.render(pages, work, "scene")

    # 4. One clip per scene, then crossfade them together. The logo, tag and footer sit
    #    in the same place on every scene, so only the message changes on screen.
    vids = []
    for i, (png, d) in enumerate(zip(pngs, durs)):
        vid = work / f"scene-{i + 1}.mp4"
        _run(["ffmpeg", "-y", "-loop", "1", "-framerate", str(FPS), "-i", str(png), "-t", f"{d:.3f}",
              "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
              "-tune", "stillimage", "-r", str(FPS), str(vid)])
        vids.append(vid)

    inputs, chain, offset, prev = [], [], 0.0, "[0:v]"
    for v in vids:
        inputs += ["-i", str(v)]
    for i in range(1, n):
        offset += durs[i - 1] - FADE
        label = f"[v{i}]"
        chain.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={offset:.3f}{label}")
        prev = label
    out = out_dir / "reel.mp4"
    video_map = prev if chain else "0:v"
    args = ["ffmpeg", "-y", *inputs, "-i", str(audio)]
    if chain:
        args += ["-filter_complex", ";".join(chain)]
    args += ["-map", video_map, "-map", f"{n}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(out)]
    _run(args)
    return out
