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

# Negation patterns: detects "ikke" or "aldri" followed by any text up to sentence boundary
# All labels within this span are extracted (e.g., "aldri rik eller fattig" finds both)
NEGATION_PATTERNS = [
    r"(?is)\b(?:ikke|aldri)\b[^.!?]*",
]
