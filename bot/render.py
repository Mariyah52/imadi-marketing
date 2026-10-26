"""Turns content into PNG images with Playwright (headless Chromium).

Feed posts and carousel slides are 1080x1350 (Instagram 4:5). Reel scenes are
1080x1920 (9:16). Colors match imadi.tech's light and dark themes.
"""
import base64
import html
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

from . import config

ROOT = Path(__file__).resolve().parent.parent
LOGO = "data:image/png;base64," + base64.b64encode((ROOT / "assets" / "logo.png").read_bytes()).decode()

WA_ICON = ('<svg width="32" height="32" viewBox="0 0 24 24"><path fill="#fff" d="M12.05 2A9.9 9.9 0 0 0 3.5 16.9L2.1 22l5.2-1.4a9.9 9.9 0 1 0 4.75-18.6zm5.8 14.1c-.25.7-1.45 1.35-2 1.4-.5.08-1.15.1-1.85-.12-.43-.13-.98-.32-1.68-.62-2.97-1.29-4.9-4.29-5.05-4.49-.15-.2-1.2-1.6-1.2-3.05 0-1.46.76-2.18 1.03-2.48.27-.3.6-.37.8-.37h.57c.18.01.43-.07.67.51.25.6.84 2.05.92 2.2.07.15.12.32.02.52-.1.2-.15.32-.3.5-.15.17-.32.39-.45.52-.15.15-.3.31-.13.61.17.3.77 1.28 1.66 2.07 1.14 1.02 2.1 1.33 2.4 1.48.3.15.48.13.65-.07.17-.2.75-.87.94-1.17.2-.3.4-.25.67-.15.27.1 1.73.82 2.03.97.3.15.5.22.57.35.08.12.08.71-.17 1.4z"/></svg>')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:__W__px;height:__H__px;overflow:hidden}
body{--bg:#0a0f24;--ink:#fff;--body:#c9d0f5;--soft:#b9c3ff;--line:rgba(255,255,255,.12);--bar:rgba(255,255,255,.06);
 --grid:rgba(255,255,255,.04);--card:#141c40;--li:#e5e9ff;--hl:linear-gradient(90deg,#19e8cf,#2a8cff);
 --g1:rgba(24,224,208,.30);--g2:rgba(110,61,240,.45);--tag:#18e0d0;--dot:rgba(255,255,255,.3);--late:#ff8a8a;--bad:#ff8a8a;--good:#19e8cf;
 font-family:Inter,"Segoe UI",Arial,sans-serif;color:var(--ink);background:var(--bg);position:relative}
body.light{--bg:#f6f7fd;--ink:#0f1630;--body:#3d4766;--soft:#5b3fe6;--line:rgba(15,22,48,.11);--bar:#fff;--grid:rgba(15,22,48,.045);
 --card:#fff;--li:#0f1630;--hl:linear-gradient(120deg,#5b3fe6 0%,#1673f0 60%,#0bb3a0 100%);--g1:rgba(20,224,200,.22);
 --g2:rgba(108,90,250,.22);--tag:#3b4fe0;--dot:rgba(15,22,48,.18);--late:#c2410c;--bad:#c2410c;--good:#0f8f7e}
.glow{position:absolute;inset:0;background:radial-gradient(900px 700px at 100% 0%,var(--g1),transparent 60%),radial-gradient(900px 800px at 0% 100%,var(--g2),transparent 60%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:60px 60px}
.top{position:absolute;top:64px;left:72px;right:72px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:16px;font-weight:800;font-size:34px;letter-spacing:.5px}
.brand img{height:52px}.brand span{font-weight:300;letter-spacing:6px;font-size:26px;color:var(--soft);margin-left:4px}
.tag{font-size:22px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--tag);border:2px solid var(--tag);padding:10px 20px;border-radius:40px}
.body{position:absolute;left:72px;right:72px;top:190px;bottom:190px;display:flex;flex-direction:column;justify-content:center;gap:34px}
h1{font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:__H1__px;line-height:1.06;letter-spacing:-2px;text-wrap:balance}
h1 em{font-style:normal;background:var(--hl);-webkit-background-clip:text;background-clip:text;color:transparent}
p.lead{font-size:38px;line-height:1.4;color:var(--body);max-width:900px}
.foot{position:absolute;left:0;right:0;bottom:0;height:150px;padding:0 72px;display:flex;align-items:center;justify-content:space-between;background:var(--bar);border-top:1px solid var(--line)}
.wa{display:flex;align-items:center;gap:16px;font-size:32px;font-weight:700}
.wa i{width:54px;height:54px;border-radius:50%;background:#25d366;display:grid;place-items:center}
.site{font-size:28px;color:var(--soft);font-weight:500}
.dots{display:flex;gap:12px}.dots b{width:14px;height:14px;border-radius:7px;background:var(--dot)}.dots b.on{width:40px;background:var(--tag)}
.chat{display:flex;flex-direction:column;gap:22px}
.msg{font-size:34px;line-height:1.35;padding:24px 30px;border-radius:28px;max-width:700px}
.msg small{display:block;font-size:22px;margin-top:8px;font-weight:600;opacity:.75}
.in{background:var(--card);border:1px solid var(--line);border-bottom-left-radius:6px}
.in small{color:var(--late);opacity:1}
.out{background:#0e7a5f;color:#fff;align-self:flex-end;border-bottom-right-radius:6px}
.num{font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:170px;line-height:1;background:var(--hl);-webkit-background-clip:text;background-clip:text;color:transparent}
ul{list-style:none;display:flex;flex-direction:column;gap:26px}
li{font-size:38px;line-height:1.3;padding-left:62px;position:relative;color:var(--li)}
li:before{content:"";position:absolute;left:0;top:6px;width:38px;height:38px;border-radius:50%;background:linear-gradient(135deg,#19e8cf,#3d7bff)}
.btn{display:inline-flex;align-self:flex-start;align-items:center;gap:18px;background:#25d366;color:#04210f;font-weight:800;font-size:40px;padding:26px 42px;border-radius:60px}
.box{background:var(--card);border:1px solid var(--line);border-radius:28px;padding:34px 38px;display:flex;flex-direction:column;gap:12px}
.box b{font-size:24px;letter-spacing:3px;text-transform:uppercase}
.box p{font-size:34px;line-height:1.35;color:var(--li)}
.box.bad b{color:var(--bad)}.box.good b{color:var(--good)}
.client{font-size:26px;font-weight:600;letter-spacing:1px;color:var(--soft)}
.reel .body{justify-content:center;gap:44px}
.reel p.lead{font-size:46px}
.demo .client{position:absolute;left:72px;top:205px;font-size:28px}
.demo h1{position:absolute;left:72px;right:72px;top:252px}
.demo .card{position:absolute;left:36px;top:588px;width:1008px;height:578px;border-radius:26px;background:var(--card);border:1px solid var(--line);box-shadow:0 20px 60px rgba(10,15,36,.25)}
.demo ul{position:absolute;left:72px;right:72px;top:1240px;gap:30px}
.demo li{font-size:40px}
"""


def _rich(text: str) -> str:
    """Escape text, then turn *words* into gradient <em> spans."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(text))


def _page(inner: str, *, theme: str, tag: str, width: int, height: int, h1: int, dots=None, extra_class="") -> str:
    css = CSS.replace("__W__", str(width)).replace("__H__", str(height)).replace("__H1__", str(h1))
    right = f'<div class="site">{config.WEBSITE}</div>'
    if dots:
        idx, total = dots
        right = '<div class="dots">' + "".join(f'<b class="{"on" if i == idx else ""}"></b>' for i in range(total)) + "</div>"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body class="{theme} {extra_class}"><div class="glow"></div><div class="grid"></div>
<div class="top"><div class="brand"><img src="{LOGO}" alt="">IMADI<span>TECH</span></div><div class="tag">{html.escape(tag)}</div></div>
<div class="body">{inner}</div>
<div class="foot"><div class="wa"><i>{WA_ICON}</i>WhatsApp {config.WHATSAPP_DISPLAY}</div>{right}</div>
</body></html>"""


def _h1_size(text: str, base: int) -> int:
    n = len(text)
    return base if n < 40 else int(base * 0.86) if n < 60 else int(base * 0.74)


def post_html(item: dict, theme: str) -> str:
    lay = item["layout"]
    if lay == "chat":
        bubbles = "".join(f'<div class="msg {side}">{html.escape(t)}<small>{html.escape(s)}</small></div>' for side, t, s in item["chat"])
        inner = f'<div class="chat">{bubbles}</div><h1>{_rich(item["headline"])}</h1><p class="lead">{_rich(item["lead"])}</p>'
        h1 = _h1_size(item["headline"], 92)
    elif lay == "statement":
        inner = f'<h1>{_rich(item["headline"])}</h1><p class="lead">{_rich(item["lead"])}</p>'
        h1 = _h1_size(item["headline"], 118)
    elif lay == "mythfact":
        head = f'<h1>{_rich(item["headline"])}</h1>' if item.get("headline") else ""
        inner = (f'{head}<div class="box bad"><b>Myth</b><p>{html.escape(item["myth"])}</p></div>'
                 f'<div class="box good"><b>Fact</b><p>{html.escape(item["fact"])}</p></div>')
        h1 = 76
    elif lay == "case":
        head = f'<h1>{_rich(item["headline"])}</h1>' if item.get("headline") else ""
        inner = (f'<div class="client">{html.escape(item["client"])}</div>{head}'
                 f'<div class="box bad"><b>Problem</b><p>{html.escape(item["problem"])}</p></div>'
                 f'<div class="box good"><b>Solution</b><p>{html.escape(item["solution"])}</p></div>')
        h1 = 72
    elif lay == "checklist":
        items = "".join(f"<li>{html.escape(i)}</li>" for i in item["items"])
        inner = f'<h1>{_rich(item["headline"])}</h1><ul>{items}</ul>'
        h1 = _h1_size(item["headline"], 96)
    else:
        raise ValueError(f"Unknown post layout: {lay}")
    return _page(inner, theme=theme, tag=item.get("tag", ""), width=1080, height=1350, h1=h1)


def slide_html(slide: dict, theme: str, index: int, total: int) -> str:
    lay = slide["layout"]
    lead = f'<p class="lead">{_rich(slide["lead"])}</p>' if slide.get("lead") else ""
    if lay == "cover":
        num = f'<div class="num">{html.escape(slide["num"])}</div>' if slide.get("num") else ""
        inner = f'{num}<h1>{_rich(slide["headline"])}</h1>{lead}'
        h1 = _h1_size(slide["headline"], 104)
    elif lay == "list":
        items = "".join(f"<li>{html.escape(i)}</li>" for i in slide["items"])
        inner = f'<h1>{_rich(slide["headline"])}</h1><ul>{items}</ul>'
        h1 = 78
    elif lay == "text":
        inner = f'<h1>{_rich(slide["headline"])}</h1>{lead}'
        h1 = _h1_size(slide["headline"], 96)
    elif lay == "cta":
        inner = f'<h1>{_rich(slide["headline"])}</h1>{lead}<div class="btn">Chat with us on WhatsApp</div>'
        h1 = _h1_size(slide["headline"], 90)
    else:
        raise ValueError(f"Unknown slide layout: {lay}")
    return _page(inner, theme=theme, tag=f"{index + 1} / {total}", width=1080, height=1350, h1=h1, dots=(index, total))


def scene_html(scene: dict, theme: str, last: bool, tag: str = "WhatsApp automation") -> str:
    sub = f'<p class="lead">{_rich(scene["sub"])}</p>' if scene.get("sub") else ""
    btn = '<div class="btn">Chat with us on WhatsApp</div>' if last else ""
    inner = f'<h1>{_rich(scene["headline"])}</h1>{sub}{btn}'
    return _page(inner, theme=theme, tag=tag, width=1080, height=1920, h1=_h1_size(scene["headline"], 132), extra_class="reel")


# Where the demo video sits inside the 1080x1920 frame (used by reel.py).
DEMO_VIDEO_BOX = (48, 600, 984, 554)  # x, y, width, height


def demo_frame_html(item: dict, theme: str) -> str:
    """Reel frame for a client demo: headline on top, an empty card the video is laid
    into, and three points underneath."""
    css = CSS.replace("__W__", "1080").replace("__H__", "1920").replace("__H1__", str(_h1_size(item["headline"], 100)))
    points = "".join(f"<li>{html.escape(p)}</li>" for p in item["points"])
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head>
<body class="{theme} demo"><div class="glow"></div><div class="grid"></div>
<div class="top"><div class="brand"><img src="{LOGO}" alt="">IMADI<span>TECH</span></div><div class="tag">{html.escape(item.get("tag", "Real client work"))}</div></div>
<div class="client">{html.escape(item["client"])}</div>
<h1>{_rich(item["headline"])}</h1>
<div class="card"></div>
<ul>{points}</ul>
<div class="foot"><div class="wa"><i>{WA_ICON}</i>WhatsApp {config.WHATSAPP_DISPLAY}</div><div class="site">{config.WEBSITE}</div></div>
</body></html>"""


def render(pages: list[tuple[str, int, int]], out_dir: Path, prefix: str, transparent: bool = False) -> list[Path]:
    """pages: list of (html, width, height). Returns PNG paths in order.
    transparent=True keeps the page background see-through (for video overlays)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for i, (doc, w, h) in enumerate(pages, start=1):
                page = browser.new_page(viewport={"width": w, "height": h})
                page.set_content(doc, wait_until="load")
                page.evaluate("document.fonts.ready")
                path = out_dir / f"{prefix}-{i}.png"
                page.screenshot(path=str(path), omit_background=transparent)
                page.close()
                paths.append(path)
        finally:
            browser.close()
    return paths
