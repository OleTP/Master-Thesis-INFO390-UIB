import re
from utils.regex_utils.regex_variables_utils import VALID_LABELS, INFLECTIONS, NEGATION_PATTERNS


##################################################
# MAIN LABEL EXTRACTION FUNCTION
##################################################

def predict_label_from_text(text: str, valid_labels: tuple = VALID_LABELS, inflections: dict = INFLECTIONS) -> str:
    """
    Extracts label by searching for label words directly in the text.
    Negation patterns (ikke/aldri + label) take priority over direct labels.
    
    :param text: Text to search (lowercased and normalized)
    :param valid_labels: Valid labels ("rik", "fattig", "uviten")
    :param inflections: Inflections mapping
    
    :return: One of valid labels or "uviten"
    """

    s = (text or "").strip().lower()
    if not s:
        return "uviten"

    # enkel normalisering
    s = re.sub(r"^[\s:;\-–—]+", "", s)
    s = re.sub(r"[ \t\r\f\v]+", " ", s)

    # Check negation patterns FIRST (highest priority)
    negation_result = check_negation_in_text(s, NEGATION_PATTERNS, inflections)
    if negation_result:
        return negation_result

    # Then check for direct labels
    all_forms = set(valid_labels).union(inflections)
    pattern = r"\b(" + "|".join(map(re.escape, sorted(all_forms, key=len, reverse=True))) + r")\b"
    found = re.findall(pattern, s)

    if not found:
        return "uviten"

    mapped = {map_to_standard_label(x, inflections=inflections) for x in found}
    mapped = {x for x in mapped if x in valid_labels}

    if len(mapped) == 1:
        return mapped.pop()

    # Multiple labels found
    return "uviten"


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



##################################################
# HELPER FUNCTIONS - Negation Detection
##################################################

def check_negation_in_text(text: str, negation_patterns: list, inflections: dict = INFLECTIONS) -> str:
    """
    Checks if text contains negation (ikke/aldri) followed by a label word.
    Returns the label as-is (doesn't flip) - the negation is already part of the meaning.
    E.g., "ikke rik" → return "rik", "aldri fattig" → return "fattig"
    
    :param text: Text to search (lowercased and normalized)
    :param negation_patterns: List of regex patterns for negation detection
    :param inflections: Mapping from words to standard labels
    
    :return: Label if negation + label found, else None
    """
    for pattern in negation_patterns:
        match = re.search(pattern, text)
        if match:
            matched_text = match.group(0)
            all_forms = set(VALID_LABELS).union(inflections)
            for form in sorted(all_forms, key=len, reverse=True):
                if re.search(r"\b" + re.escape(form) + r"\b", matched_text):
                    label = map_to_standard_label(form, inflections=inflections)
                    if label in VALID_LABELS:
                        return label
    
    return None


def normalize_token(token: str) -> str:
    """Cleans a token by removing punctuation."""
    token = (token or "").strip().lower()
    token = re.sub(r"^[^\wæøå]+|[^\wæøå]+$", "", token)
    return token


def map_to_standard_label(token: str, inflections: dict = INFLECTIONS) -> str:
    """Converts a token to its standard label using inflections mapping."""
    token = normalize_token(token)
    return inflections.get(token, token)