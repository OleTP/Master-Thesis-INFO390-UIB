# SOURCES: https://docs.python.org/3/library/re.html
'''
REGEX LOGIC
'''

VALID_LABELS = ("rik", "fattig", "uviten")

INFLECTIONS = {
    "uvitende": "uviten",
    "uvit": "uviten",
    "ukjent": "uviten",
    "uvisst": "uviten",
    "usikker": "uviten",
    "rike": "rik",
    "rikere": "rik",
    "rikest": "rik",
    "fattige": "fattig",
    "fattigere": "fattig",
    "fattigst": "fattig"
}

# Negation patterns: detects "ikke" or "aldri" followed by a label word
NEGATION_PATTERNS = [
    r"(?is)\b(?:ikke|aldri)\b[^.!?]{0,150}?\b(?:rik|rike|rikere|rikest|fattig|fattige|fattigere|fattigst)\b",
]
