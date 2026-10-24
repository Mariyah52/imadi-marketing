"""Publishes to Instagram and the Facebook Page through Meta's Graph API.

Uses one long-lived Page access token (see README.md), which can publish both to the
Facebook Page and to the Instagram Business account linked to it.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"


def _env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing {name}. Add it under GitHub > Settings > Secrets and variables > Actions.")
    return value


def _call(method: str, path: str, params: dict) -> dict:
    data = urllib.parse.urlencode(params).encode()
    url = f"{GRAPH}/{path}"
    if method == "GET":
        req = urllib.request.Request(f"{url}?{data.decode()}")
    else:
        req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"Meta API error on {path}: {body}") from None


def _wait_ready(container_id: str, token: str, tries: int = 40, every: int = 15) -> None:
    for _ in range(tries):
        status = _call("GET", container_id, {"fields": "status_code,status", "access_token": token})
        if status.get("status_code") == "FINISHED":
            return
        if status.get("status_code") == "ERROR":
            raise RuntimeError(f"Instagram could not process the media: {status}")
        time.sleep(every)
    raise RuntimeError("Instagram took too long to process the media.")


# ---------------------------------------------------------------- Instagram --
def instagram(fmt: str, urls: list[str], caption: str) -> str:
    ig = _env("IG_USER_ID")
    token = _env("META_PAGE_TOKEN")
    if fmt == "post":
        c = _call("POST", f"{ig}/media", {"image_url": urls[0], "caption": caption, "access_token": token})
    elif fmt == "carousel":
        kids = []
        for u in urls:
            k = _call("POST", f"{ig}/media", {"image_url": u, "is_carousel_item": "true", "access_token": token})
            _wait_ready(k["id"], token, every=5)
            kids.append(k["id"])
        c = _call("POST", f"{ig}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": caption, "access_token": token})
    elif fmt == "reel":
        c = _call("POST", f"{ig}/media", {"media_type": "REELS", "video_url": urls[0], "caption": caption,
                                           "share_to_feed": "true", "access_token": token})
    else:
        raise ValueError(fmt)
    _wait_ready(c["id"], token)
    return _call("POST", f"{ig}/media_publish", {"creation_id": c["id"], "access_token": token})["id"]


# ----------------------------------------------------------------- Facebook --
def facebook(fmt: str, urls: list[str], caption: str) -> str:
    page = _env("FB_PAGE_ID")
    token = _env("META_PAGE_TOKEN")
    if fmt == "post":
        return _call("POST", f"{page}/photos", {"url": urls[0], "caption": caption, "access_token": token})["id"]
    if fmt == "carousel":
        ids = [_call("POST", f"{page}/photos", {"url": u, "published": "false", "access_token": token})["id"] for u in urls]
        params = {"message": caption, "access_token": token}
        for i, pid in enumerate(ids):
            params[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
        return _call("POST", f"{page}/feed", params)["id"]
    if fmt == "reel":
        return _call("POST", f"{page}/videos", {"file_url": urls[0], "description": caption, "access_token": token})["id"]
    raise ValueError(fmt)
