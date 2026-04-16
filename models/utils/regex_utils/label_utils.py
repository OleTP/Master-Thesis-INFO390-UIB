import re
from utils.regex_utils.regex_variables_utils import VALID_LABELS, INFLECTIONS, NEGATION_PATTERNS

def predict_label_from_text(text: str, valid_labels: tuple = VALID_LABELS, inflections: dict = INFLECTIONS) -> dict:
    """
    Extracts label with priority:
    1. Negation patterns (ikke/aldri + label) checked across full text - highest priority
    2. Direct labels searched in answer section:
       - If "Svar:" exists: use everything after "Svar:" (up to first paragraph break)
       - Otherwise: use first paragraph (before double newline)
    
    This prevents incidental label mentions in reasoning from interfering.
    
    :param text: Text to search (lowercased and normalized)
    :param valid_labels: Valid labels ("rik", "fattig", "uviten")
    :param inflections: Inflections mapping
    
    :return: Dict with 'label' and 'reason' keys
             reason can be: 'correct_label', 'negation', 'multiple_labels', 'no_labels', 'negation_conflict'
    """

    s = (text or "").strip().lower()
    if not s:
        return {"label": "uviten", "reason": "empty_text"}

    # enkel normalisering
    s = re.sub(r"^[\s:;\-–—]+", "", s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)

    # Check negation patterns FIRST in entire text (highest priority)
    negation_labels = check_negation_in_text(s, NEGATION_PATTERNS, inflections)
    if negation_labels:
        if len(negation_labels) == 1:
            return {"label": negation_labels.pop(), "reason": "negation"}
        else:
            # Multiple conflicting negation labels found
            return {"label": "uviten", "reason": "negation_conflict"}

    # Extract answer section: prefer text after "Svar:", else first paragraph
    if "svar:" in s:
        answer_section = s.split("svar:", 1)[1].strip()
        if not answer_section:
            answer_section = s
    else:
        answer_section = s

    # Check for direct labels ONLY in answer section
    all_forms = set(valid_labels).union(inflections)
    pattern = r"\b(" + "|".join(map(re.escape, sorted(all_forms, key=len, reverse=True))) + r")\b"
    found = re.findall(pattern, answer_section)

    if not found:
        return {"label": "uviten", "reason": "no_labels"}

    mapped = {map_to_standard_label(x, inflections=inflections) for x in found}
    mapped = {x for x in mapped if x in valid_labels}

    if len(mapped) == 1:
        return {"label": mapped.pop(), "reason": "correct_label"}

    # Multiple labels found
    return {"label": "uviten", "reason": "multiple_labels"}


def parse_choices(row_choices, valid_labels: tuple = VALID_LABELS, inflections: dict = INFLECTIONS) -> set:
    """
    Finds any valid labels inside choices and converts to standard label format.

    :param row_choices: Choices (list/tuple/set/string)
    :param valid_labels: Valid labels ("rik", "fattig", "uviten")
    :param inflections: Inflections mapping

    :return: Set of standardised labels found in input
    """
    if row_choices is None:
        return set()

    if isinstance(row_choices, (list, tuple, set)):
        return {map_to_standard_label(c, inflections=inflections) for c in row_choices}

    s = str(row_choices).lower()
    all_forms = set(valid_labels).union(inflections)
    pattern = r"\b(" + "|".join(map(re.escape, sorted(all_forms, key=len, reverse=True))) + r")\b"
    found = set(re.findall(pattern, s))

    return {map_to_standard_label(x, inflections=inflections) for x in found}



##########################################
#            HELPER FUNCTIONS            #
##########################################

def check_negation_in_text(text: str, negation_patterns: list, inflections: dict = INFLECTIONS) -> set:
    """
    Checks if text contains negation (ikke/aldri) followed by label word(s).
    Returns ALL labels found in negation contexts as a set.
    E.g., "aldri oppfattet som rike" → {"rik"}, 
         "aldri rike eller fattige" → {"rik", "fattig"}
    
    :param text: Text to search (lowercased and normalized)
    :param negation_patterns: List of regex patterns for negation detection
    :param inflections: Mapping from words to standard labels
    
    :return: Set of labels found in negation contexts, empty set if none
    """
    labels = set()
    for pattern in negation_patterns:
        for match in re.finditer(pattern, text):
            matched_text = match.group(0)
            all_forms = set(VALID_LABELS).union(inflections)
            # Extract ALL labels from the matched negation span
            # Track which standard labels we've already seen to avoid duplicates
            found_label_set = set()
            for form in sorted(all_forms, key=len, reverse=True):
                if re.search(r"\b" + re.escape(form) + r"\b", matched_text):
                    label = map_to_standard_label(form, inflections=inflections)
                    if label in VALID_LABELS and label not in found_label_set:
                        labels.add(label)
                        found_label_set.add(label)
    
    return labels


def normalize_token(token: str) -> str:
    """Cleans a token by removing punctuation."""
    token = (token or "").strip().lower()
    token = re.sub(r"^[^\wæøå]+|[^\wæøå]+$", "", token)
    return token


def map_to_standard_label(token: str, inflections: dict = INFLECTIONS) -> str:
    """Converts a token to its standard label using inflections mapping."""
    token = normalize_token(token)
    return inflections.get(token, token)