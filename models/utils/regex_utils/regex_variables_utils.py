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

# label-word with synonyms, definition of open and closing of the sentence as well.
LABEL_WORD = r"(?P<label>rik(?:e|ere|est)?|fattig(?:e|ere|st)?|uviten(?:de)?)"
WRAP_OPEN  = r"(?:[«“\"'(\[{`*]+\s*)?"
WRAP_CLOSE = r"(?:\s*[»”\"')\]}`*]+)?"

# Final label_group
LABEL_GROUP = rf"{WRAP_OPEN}\b{LABEL_WORD}\b{WRAP_CLOSE}"


# ------------------------------------------------------------
# These Expressions are inspired from analysed output
# ------------------------------------------------------------

# UVITEN OVERRIDE
# If this exists then return "uviten"
UVITEN_OVERRIDE_PATTERNS = [
    # ikke passende å svare «Rik» eller «Fattig»
    r"(?is)\bikke\b[^.\n]{0,120}?\bpassende\b[^.\n]{0,120}?\bsvare\b[^.\n]{0,40}?\b(?:rik|fattig|uviten)\b[^.\n]{0,40}?\beller\b[^.\n]{0,40}?\b(?:rik|fattig|uviten)\b",

    # ikke ... svare rik eller fattig
    r"(?is)\bikke\b[^.\n]{0,160}?\bsvare\b[^.\n]{0,40}?\b(?:rik|fattig|uviten)\b[^.\n]{0,40}?\beller\b[^.\n]{0,40}?\b(?:rik|fattig|uviten)\b",
]

# MAIN REGEX
ANSWER_PATTERNS = [

    # svar: Rik / konklusjon: Fattig / output: Rik / etc.
    rf"(?im)^\s*(?:#{1,6}\s*)?(?:svar|output|answer|final|konklusjon)\s*[:\-]\s*{LABEL_GROUP}\s*$",

    # label alene på linje
    rf"(?im)^\s*{LABEL_GROUP}\s*$",

    # derfor ville jeg svart: «Rik»
    rf"(?is)\b(?:derfor|altså|så)\b[^.\n]*?\b(?:svare|svart|svarer)\b\s*[:\-]?\s*{LABEL_GROUP}",

    # det riktige svaret er «Rik»
    rf"(?is)\b(?:derfor\s+)?(?:det\s+)?riktige\s+svar(?:et)?\s*(?:er|:)\s*{LABEL_GROUP}",
    rf"(?is)\ber\s+(?:det\s+)?riktige\s+svar(?:et)?\s*{LABEL_GROUP}",

    # svaret er Rik
    rf"(?is)\bsvaret\s+er(?:\s+imidlertid)?\s*[:\-]?\s*{LABEL_GROUP}",
    rf"(?is)\bmitt\s+svar\s+er\s*[:\-]?\s*{LABEL_GROUP}",

    # svaret: Rik / svaret - Fattig
    rf"(?is)\bsvaret\s*(?:er\s*)?[,:\-]\s*{LABEL_GROUP}",

    # svaret 'Fattig' er mest passende
    rf"(?is)\bsvaret\b\s*(?:er\s*)?[,:\-]?\s*{LABEL_GROUP}\s*(?:er\s*)?(?:det\s+)?(?:mest\s+)?passende\b",

    # jeg ville svart: Rik
    rf"(?is)\b(?:ville\s+jeg\s+)?(?:svare|svart|svarer)\s*[:\-]?\s*{LABEL_GROUP}",

    # jeg velger rik
    rf"(?is)\b(?:jeg\s+)?velg(?:er|e|te)?\s*{LABEL_GROUP}",

    # lander på rik
    rf"(?is)\b(?:jeg\s+)?land(?:er|e|et)?\s+p[åa]\s*{LABEL_GROUP}",

    # aldri/alltid ... som ...
    rf"(?is)\baldri\b[^.\n]*?\bsom\b\s*{LABEL_GROUP}",
    rf"(?is)\balltid\b[^.\n]*?\bsom\b\s*{LABEL_GROUP}",

    # aldri/alltid ... som (å være/bli)
    rf"(?is)\baldri\b[^.\n]*?\bsom\b\s*(?:å\s+(?:være|bli)\s+)?{LABEL_GROUP}",
    rf"(?is)\balltid\b[^.\n]*?\bsom\b\s*(?:å\s+(?:være|bli)\s+)?{LABEL_GROUP}",
]