"""Settings for the IMADI Tech marketing bot.

Everything Maria might want to change lives in this one file. Secrets (Meta tokens)
are never stored here: they live in GitHub Actions secrets, see README.md.
"""
from datetime import date

BRAND = "IMADI Tech"
WEBSITE = "imadi.tech"
WEBSITE_URL = "https://www.imadi.tech/whatsapp-automation/"
WHATSAPP_DISPLAY = "0315 3205484"
WHATSAPP_LINK = "https://wa.me/923153205484"

# Posting times in Pakistan time (UTC+5). The workflow's cron lines in
# .github/workflows/post.yml must match these hours (cron runs in UTC).
SLOT_HOURS_PKT = {"morning": 11, "afternoon": 15, "evening": 19}

# Full weekly schedule Maria asked for (13 posts a week). Monday = 0 ... Sunday = 6.
FULL_SCHEDULE = {
    0: {"morning": "carousel", "afternoon": "reel", "evening": "post"},       # Monday
    1: {"morning": "post", "evening": "carousel"},                             # Tuesday
    2: {"morning": "reel", "evening": "post"},                                 # Wednesday
    3: {"morning": "carousel", "evening": "reel"},                             # Thursday
    4: {"morning": "post", "afternoon": "carousel", "evening": "reel"},       # Friday
    5: {"morning": "post"},                                                    # Saturday
    6: {},                                                                     # Sunday off
}

# Warm-up: the Instagram account was recently restored, so for the first week the
# bot posts only once a day (the evening slot of the full schedule, or the only
# slot that day). After WARMUP_UNTIL it switches to FULL_SCHEDULE automatically.
# To skip the warm-up, set WARMUP_UNTIL = date(2000, 1, 1).
WARMUP_UNTIL = date(2026, 11, 2)
WARMUP_SCHEDULE = {
    0: {"evening": "reel"},
    1: {"evening": "carousel"},
    2: {"evening": "post"},
    3: {"evening": "reel"},
    4: {"evening": "carousel"},
    5: {"morning": "post"},
    6: {},
}

# Counting starts here, so light/dark and the two voices alternate post by post.
EPOCH = date(2026, 10, 26)

# American English neural voices (free, via edge-tts). Reels alternate between them.
VOICES = ["en-US-AvaMultilingualNeural", "en-US-AndrewMultilingualNeural"]

# Where to post. Instagram can be switched off until the account is linked.
POST_TO_INSTAGRAM = True
POST_TO_FACEBOOK = True
