from presidio_analyzer import Pattern, PatternRecognizer
from typing import Optional, List, Tuple

class AUBankAccountNumber(PatternRecognizer):
    """
    Recognizes Indian UIDAI Person Identification Number ("AADHAAR").

    Reference: https://en.wikipedia.org/wiki/Aadhaar
    A 12 digit unique number that is issued to each individual by Government of India
    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    :param replacement_pairs: List of tuples with potential replacement values
    for different strings to be used during pattern matching.
    This can allow a greater variety in input, for example by removing dashes or spaces.
    """

    PATTERNS = [
        Pattern(
            "AUBankAccountNumber (medium)",
            r"\b(\d{3}[- ]?\d{3})[- ]?(\d{6,10})\b",
            0.4,
        ),
        Pattern(
            "AUBankAccountNumber (weak)",
            r"\b(\d{3}[- ]?\d{3})[- ]?(\d{5,9})\b",
            0.3,
        )
    ]

    CONTEXT = [
        "correspondent bank",
        "base currency",
        "holder address",
        "bank address",
        "information account",
        "fund transfers",
        "bank charges",
        "bank details",
        "banking information",
        "iaea"
    ]

    utils = None

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "AU_BANK_ACCOUNT_NUMBER",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )