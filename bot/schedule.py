"""Works out what to post for a given slot, and keeps the rotation counters.

The counters are computed from the calendar (no stored state), so every run gets the
same answer: post number N since EPOCH decides light/dark, and the Nth post of a
format decides which template and which voice it uses.
"""
from datetime import date, datetime, timedelta, timezone

from . import config

PKT = timezone(timedelta(hours=5))
SLOT_ORDER = ["morning", "afternoon", "evening"]


def schedule_for(day: date) -> dict:
    table = config.WARMUP_SCHEDULE if day < config.WARMUP_UNTIL else config.FULL_SCHEDULE
    return table.get(day.weekday(), {})


def slot_from_hour(hour_pkt: int) -> str:
    """Nearest configured slot to an hour (GitHub's cron can start a few minutes late)."""
    return min(config.SLOT_HOURS_PKT, key=lambda s: abs(config.SLOT_HOURS_PKT[s] - hour_pkt))


def counters(day: date, slot: str, fmt: str) -> tuple[int, int]:
    """(overall post number, number of earlier posts of this format), both from EPOCH."""
    overall = 0
    same_format = 0
    d = config.EPOCH
    while d <= day:
        for s in SLOT_ORDER:
            if d == day and s == slot:
                return overall, same_format
            f = schedule_for(d).get(s)
            if f:
                overall += 1
                if f == fmt:
                    same_format += 1
        d += timedelta(days=1)
    return overall, same_format


def plan(now: datetime | None = None, slot: str | None = None, force_format: str | None = None) -> dict | None:
    now = (now or datetime.now(timezone.utc)).astimezone(PKT)
    day = now.date()
    slot = slot or slot_from_hour(now.hour)
    fmt = force_format or schedule_for(day).get(slot)
    if not fmt:
        return None
    overall, nth = counters(max(day, config.EPOCH), slot, fmt)
    return {
        "date": day.isoformat(),
        "weekday": now.strftime("%A"),
        "slot": slot,
        "format": fmt,
        "theme": "light" if overall % 2 == 0 else "dark",
        "nth": nth,
        "voice": config.VOICES[nth % len(config.VOICES)],
    }
