import re

_TR_MAP = str.maketrans({
    "ç": "c", "Ç": "c",
    "ğ": "g", "Ğ": "g",
    "ı": "i", "I": "i", "İ": "i",
    "ö": "o", "Ö": "o",
    "ş": "s", "Ş": "s",
    "ü": "u", "Ü": "u",
})

_ALLOWED_RE = re.compile(r"[^a-zA-Z0-9_]")

def normalize_community_name(raw: str) -> str:
    if raw is None:
        return ""

    s = raw.strip()
    s = s.translate(_TR_MAP)
    s = s.lower()
    s = re.sub(r"\s+", "-", s)          
    s = re.sub(r"-{2,}", "-", s)        
    s = _ALLOWED_RE.sub("", s)        
    s = s.strip("-_")                   
    return s