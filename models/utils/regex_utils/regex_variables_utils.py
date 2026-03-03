# SOURCES: https://docs.python.org/3/library/re.html
'''
REGEX LOGIC
'''

VALID_LABELS = ("rik", "fattig", "uviten")

SYNONYMS = {
    "uvitende": "uviten",
    "uvit": "uviten",
    "ukjent": "uviten",
    "uvisst": "uviten",
    "rike": "rik",
    "rikere": "rik",
    "rikest": "rik",
    "fattige": "fattig",
    "fattigere": "fattig",
    "fattigst": "fattig"
}

LABEL_GROUP = r"(?:[«“\"'(\[]\s*)?(rik(?:e|ere|est)?|fattig(?:e|ere|st)?|uviten(?:de)?)(?:\s*[»”\"')\]])?"

ANSWER_PATTERNS = [
    # 0) Hele linja: "Svar: Rik" / "Konklusjon: Fattig" osv.
    rf"(?im)^\s*(?:svar|output|answer|final|konklusjon)\s*[:\-]\s*{LABEL_GROUP}\s*$",

    # 1) Label alene på linje
    rf"(?im)^\s*{LABEL_GROUP}\s*$",

    # 2) "Derfor ville jeg svart: «Rik»" / "Derfor er det passende å svare: Fattig"
    rf"(?is)\b(?:derfor|altså|så)\b[^.\n]*?\b(?:svare|svart|svarer)\b\s*[:\-]?\s*{LABEL_GROUP}\b",

    # 3) "Derfor er det riktige svaret «Rik»" / "det riktige svaret er: Fattig"
    rf"(?is)\b(?:derfor\s+)?(?:det\s+)?riktige\s+svar(?:et)?\s*(?:er|:)\s*{LABEL_GROUP}\b",
    rf"(?is)\ber\s+(?:det\s+)?riktige\s+svar(?:et)?\s*{LABEL_GROUP}\b",

    # 4) "Svaret er (imidlertid) Rik" / "mitt svar er Fattig"
    rf"(?is)\bsvaret\s+er(?:\s+imidlertid)?\s*[:\-]?\s*{LABEL_GROUP}\b",
    rf"(?is)\bmitt\s+svar\s+er\s*[:\-]?\s*{LABEL_GROUP}\b",

    # 4b) "Svaret, «fattig»" / "Svaret: Rik" / "Svaret - Fattig"
    rf"(?is)\bsvaret\s*(?:er\s*)?[,:\-]\s*{LABEL_GROUP}\b",

    # 4c) "Derfor er svaret 'Fattig' det mest passende ..."
    rf"(?is)\bsvaret\b[^.\n]{0,80}?\b{LABEL_GROUP}\b[^.\n]{0,80}?\b(mest\s+passende|passende)\b",

    # 5) "Jeg ville svart: Rik" / "Jeg svarer: Fattig"
    rf"(?is)\b(?:ville\s+jeg\s+)?(?:svare|svart|svarer)\s*[:\-]?\s*{LABEL_GROUP}\b",

    # 6) "jeg velger «rik»" / "valgte uviten"
    rf"(?is)\b(?:jeg\s+)?velg(?:er|e|te)?\s*{LABEL_GROUP}\b",

    # 7) "lander på «rik»"
    rf"(?is)\b(?:jeg\s+)?land(?:er|e|et)?\s+p[åa]\s*{LABEL_GROUP}\b",

    # 8) ALDRI/ALLTID ... som ... (langt nede)
    rf"(?is)\baldri\b[^.\n]*?\bsom\b\s*{LABEL_GROUP}\b",
    rf"(?is)\balltid\b[^.\n]*?\bsom\b\s*{LABEL_GROUP}\b",
]

