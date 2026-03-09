import re
from utils.regex_utils.regex_variables_utils import VALID_LABELS, SYNONYMS, ANSWER_PATTERNS, UVITEN_OVERRIDE_PATTERNS

def predict_label_from_text(text: str, valid_labels: tuple=VALID_LABELS, synonyms: dict=SYNONYMS, 
                            answer_patterns: list=ANSWER_PATTERNS, uviten_override_patterns: list = UVITEN_OVERRIDE_PATTERNS) -> str:
    """
    The function looks for a label in the text using regex patterns.
    If it finds a match, it converts the label to a standard form
    (for example mapping "rike" to "rik").

    :param text: Text from the model output
    :param valid_labels: The Valid labels ("rik", "fattig", "uviten")
    :param synonyms: Mapping from alternative words to standard labels. 
    :param answer_patterns: Regex patterns used to detect labels.

    :return: One of the valid_labels ("rik", "fattig", "uviten"), if no pattern is found it returns "uviten".
    """
    s = (text or "").strip().lower()
    if not s:
        return "uviten"
    
    for pat in uviten_override_patterns:
        if re.search(pat, s):
            return "uviten"

    for pat in answer_patterns:
        m = re.search(pat, s)
        if m:
            label = map_to_standard_label(m.group("label"), synonyms=synonyms)
            return label if label in valid_labels else "uviten"

    return "uviten"


def parse_choices(row_choices, valid_labels: tuple=VALID_LABELS, synonyms: dict=SYNONYMS) -> set:
    """
    The function takes choices (either a list or a string). 
    Then finds any valid labels inside the choice, and converts them to the standard label format.

    :param row_choices: Any type that is stored in the 'choices' column for that row.
    :param valid_labels: The Valid labels ("rik", "fattig", "uviten")
    :param synonyms: Mapping from alternative words to standard labels. 

    :return: A set of standardised labels found in the input.  
    """
    if row_choices is None:
        return set()

    if isinstance(row_choices, (list, tuple, set)):
        return {map_to_standard_label(c, synonyms=synonyms) for c in row_choices}

    s = str(row_choices).lower()

    all_forms = set(valid_labels) | set(synonyms.keys())
    pattern = r"\b(" + "|".join(map(re.escape, sorted(all_forms, key=len, reverse=True))) + r")\b"
    found = set(re.findall(pattern, s))

    return {map_to_standard_label(x, synonyms=synonyms) for x in found}



##################################################
# HELPER FUNCTIONS for predict_label_from_text() #
##################################################
def normalize_token(token: str) -> str:
    """
    Cleans a token by lower and removing punctations.
    """
    token = (token or "").strip().lower()
    token = re.sub(r"^[^\wæøå]+|[^\wæøå]+$", "", token)
    return token

def map_to_standard_label(token: str, synonyms=SYNONYMS) -> str:
    """
    Converts a token to its standard label using the synonym mapping
    """
    token = normalize_token(token)
    return synonyms.get(token, token)

