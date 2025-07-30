import regex as re

HASHTAG_RE = re.compile(r"#(\p{L}[\p{L}\p{N}_]+)", re.UNICODE)
MENTION_RE = re.compile(r"@([A-Za-z0-9_]{1,15})")

def extract_hashtags(text: str):
    tags = [m.group(1) for m in HASHTAG_RE.finditer(text or "")]
    return tags, [t.lower() for t in tags]

def extract_mentions(text: str):
    return [{"user_id": None, "screen_name": m.group(1)} for m in MENTION_RE.finditer(text or "")]
