from presidio_analyzer import Pattern, PatternRecognizer
from typing import Optional, List, Tuple
import re

class ItPassportRecognizer(PatternRecognizer):
    """
    Recognizes IT Passport number using case-insensitive regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    PATTERNS = [
        Pattern(
            "ItPassportRecognizer (Medium)",
            r"\b[A-Z0-9]{2}\d{7}\b",
            0.3,
        ),
    ]

    CONTEXT = [
        "passport#",
        "passport #",
        "passportid",
        "passports",
        "passportno",
        "passport no",
        "passportnumber",
        "passport number",
        "passportnumbers",
        "passport numbers",
        
        "italiana passaporto",
        "passaporto italiana",
        "passaporto numero",
        "numéro passeport",
        "numero di passaporto",
        "numeri del passaporto",
        "passeport italien",

        "date of issue",
        "date of expiry"
    ]

    utils = None

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "IT_PASSPORT_NUMBER",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
        regex_flags = re.IGNORECASE
    ):
        self.replacement_pairs = (
            replacement_pairs if replacement_pairs else [("-", ""), (" ", "")]
        )   
         
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
            global_regex_flags=regex_flags
        )

        # custom attributes
        self.type = 'alphanumeric'
        self.range = (9,9)
