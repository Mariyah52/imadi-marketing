"""Runs one posting slot: decide, build, host, publish.

GitHub Actions calls this at 11am, 3pm and 7pm Pakistan time, Monday to Saturday.
It looks up what the schedule says for that slot, builds the image(s) or reel,
and posts to Instagram and Facebook. If one platform fails, the other still posts
and the run is marked failed so GitHub emails Maria.

Local test (no posting):  python -m bot.main --dry-run --format reel --theme dark
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import config, content, render, schedule

ROOT = Path(__file__).resolve().parent.parent


def captions(item: dict, nth: int) -> dict:
    body = item["caption"].strip()
    tags = content.HASHTAG_SETS[nth % len(content.HASHTAG_SETS)]
    fb = (f"{body}\n\n💬 Chat with us on WhatsApp: {config.WHATSAPP_LINK}\n"
          f"🌐 See how it works: {config.WEBSITE_URL}\n\n{tags}")
    ig = (f"{body}\n\n💬 Chat with us on WhatsApp: tap the link in our bio, or message {config.WHATSAPP_DISPLAY}.\n\n{tags}")
    return {"facebook": fb, "instagram": ig}


def build_media(plan: dict, item: dict, out: Path) -> list[Path]:
    theme = plan["theme"]
    if plan["format"] == "post":
        return render.render([(render.post_html(item, theme), 1080, 1350)], out, "post")
    if plan["format"] == "carousel":
        slides = item["slides"]
        pages = [(render.slide_html(s, theme, i, len(slides)), 1080, 1350) for i, s in enumerate(slides)]
        return render.render(pages, out, "slide")
    from . import reel
    return [reel.build(item, theme, plan["voice"], out)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot", choices=list(config.SLOT_HOURS_PKT), help="morning / afternoon / evening (default: from the clock)")
    ap.add_argument("--format", choices=["post", "carousel", "reel"], help="force a format (testing)")
    ap.add_argument("--theme", choices=["light", "dark"], help="force light or dark (testing)")
    ap.add_argument("--nth", type=int, help="force which content item to use (testing)")
    ap.add_argument("--dry-run", action="store_true", help="build the media but don't post")
    args = ap.parse_args()

    slot = args.slot or os.environ.get("SLOT") or None
    fmt = args.format or os.environ.get("FORCE_FORMAT") or None
    if fmt == "auto":
        fmt = None
    dry = args.dry_run or os.environ.get("DRY_RUN") == "1"

    plan = schedule.plan(slot=slot, force_format=fmt)
    if not plan:
        print("Nothing scheduled for this slot. See FULL_SCHEDULE / WARMUP_SCHEDULE in bot/config.py.")
        return 0
    if args.theme:
        plan["theme"] = args.theme
    if args.nth is not None:
        plan["nth"] = args.nth
        plan["voice"] = config.VOICES[args.nth % len(config.VOICES)]

    item = content.pick(plan["format"], plan["nth"])
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    out = ROOT / "output" / f"{stamp}-{plan['format']}"
    print(f"{plan['weekday']} {plan['slot']}: {plan['format']} #{plan['nth']} ({plan['theme']}, voice {plan['voice']})")

    files = build_media(plan, item, out)
    caps = captions(item, plan["nth"])
    (out / "summary.json").write_text(json.dumps({**plan, "files": [f.name for f in files], "captions": caps}, indent=2, ensure_ascii=False))
    print("Built:", ", ".join(f.name for f in files))
    if dry:
        print("Dry run: nothing posted.")
        return 0

    from . import host, meta
    urls = host.publish(files, f"{plan['date']}/{plan['slot']}-{plan['format']}")
    print("Hosted:", *urls, sep="\n  ")

    failed = []
    if config.POST_TO_INSTAGRAM:
        try:
            print("Instagram post id:", meta.instagram(plan["format"], urls, caps["instagram"]))
        except Exception as e:
            failed.append("Instagram")
            print("Instagram failed:", e, file=sys.stderr)
    if config.POST_TO_FACEBOOK:
        try:
            print("Facebook post id:", meta.facebook(plan["format"], urls, caps["facebook"]))
        except Exception as e:
            failed.append("Facebook")
            print("Facebook failed:", e, file=sys.stderr)

    if failed:
        print("Not posted to:", ", ".join(failed), file=sys.stderr)
        return 1
    print("Posted to Instagram and Facebook.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
