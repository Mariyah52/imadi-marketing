"""Gives generated images and videos a public URL.

Instagram and Facebook download media from a URL themselves, so each file is pushed
to a `media` branch of this (public) repository and served from
raw.githubusercontent.com. Runs only inside GitHub Actions, using the built-in
GITHUB_TOKEN; no extra secret is needed.
"""
import os
import shutil
import subprocess
import time
from pathlib import Path

BRANCH = "media"


def _git(*args: str, cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def publish(files: list[Path], folder: str) -> list[str]:
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    if not repo or not token:
        raise RuntimeError("Hosting needs GITHUB_REPOSITORY and GITHUB_TOKEN (only available inside GitHub Actions).")
    remote = f"https://x-access-token:{token}@github.com/{repo}.git"
    work = Path(os.environ.get("RUNNER_TEMP", "/tmp")) / "media-branch"
    shutil.rmtree(work, ignore_errors=True)

    exists = subprocess.run(["git", "ls-remote", "--exit-code", "--heads", remote, BRANCH], capture_output=True).returncode == 0
    if exists:
        subprocess.run(["git", "clone", "--depth", "1", "--branch", BRANCH, remote, str(work)], check=True, capture_output=True)
    else:
        work.mkdir(parents=True)
        _git("init", "-b", BRANCH, cwd=work)
        _git("remote", "add", "origin", remote, cwd=work)

    dest = work / folder
    dest.mkdir(parents=True, exist_ok=True)
    urls = []
    for f in files:
        shutil.copy2(f, dest / f.name)
        urls.append(f"https://raw.githubusercontent.com/{repo}/{BRANCH}/{folder}/{f.name}")

    who = ["-c", "user.name=IMADI Marketing Bot", "-c", "user.email=bot@imadi.tech"]
    _git(*who, "add", "-A", cwd=work)
    subprocess.run(["git", *who, "commit", "-m", f"Media for {folder}"], cwd=work, capture_output=True)
    _git("push", "origin", f"HEAD:{BRANCH}", cwd=work)

    # raw.githubusercontent.com takes a little while to start serving new files.
    time.sleep(45)
    return urls


def posted_today(day: str) -> set[str]:
    """Folder names already on the media branch for this date, e.g. {"evening-reel"}.
    Media is pushed just before posting, so a folder here means that slot was handled."""
    import json, urllib.request, urllib.error
    repo, token = os.environ.get("GITHUB_REPOSITORY"), os.environ.get("GITHUB_TOKEN")
    if not repo or not token:
        return set()
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/contents/{day}?ref={BRANCH}",
                                 headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return {item["name"] for item in json.load(r) if item.get("type") == "dir"}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return set()
        raise
