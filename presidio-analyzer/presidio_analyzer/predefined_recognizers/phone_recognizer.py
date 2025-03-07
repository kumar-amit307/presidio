from typing import List, Optional

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

from presidio_analyzer import (
    RecognizerResult,
    LocalRecognizer,
    AnalysisExplanation,
    EntityRecognizer,
)
from presidio_analyzer.nlp_engine import NlpArtifacts


class PhoneRecognizer(LocalRecognizer):
    """Recognize multi-regional phone numbers.

     Using python-phonenumbers, along with fixed and regional context words.
    :param context: Base context words for enhancing the assurance scores.
    :param supported_language: Language this recognizer supports
    :param supported_regions: The regions for phone number matching and validation
    :param leniency: The strictness level of phone number formats.
    Accepts values from 0 to 3, where 0 is the lenient and 3 is the most strictest.
    """

    SCORE = 0.3
    CONTEXT = [
        # english
        "phone",
        "telephone",
        "cell",
        "cellphone",
        "mobile",
        "call",
        "mob",
        "P",
        "M",
        "Ph",
        "landline",
        "dial",
        "office",
        "home",
        "work",
        "number",
        "contact",
        "reach",
        "communicate",
        "communicating",
        "cellular",
        "phone number",
        "telephone number",
        "mobile number",
        "cell phone number",
        "contact number",
        "landline number",
        "dial-in number",
        "toll-free number",
        "hotline",
        "extension number",

        # spanish
        "número de teléfono",
        "número de móvil",
        "número fijo",
        "móvil",
        "teléfono",
        "contacto",
        "teléfono móvil",
        "celular",
        "fijo",
        "número de contacto",
        "línea de emergencia",
        "número gratuito",
        "extensión",
        "línea directa",
        "número de acceso",

        # german
        "Telefonnummer",
        "Handynummer",
        "Festnetznummer",
        "Kontaktnummer",
        "Rufnummer",
        "Notrufnummer",
        "gebührenfreie Nummer",
        "Durchwahl",
        "Hotline",
        "Anschlussnummer",

        # dutch
        "telefoonnummer",
        "mobiel nummer",
        "mobiele nummer",
        "vast nummer",
        "contactnummer",
        "belnummer",
        "noodnummer",
        "gratisnummer",
        "toestelnummer",
        "helplijn",
        "aansluitnummer",

        # portuguese
        "número de telefone",
        "número de celular",
        "número de telemóvel",
        "número fixo",
        "telefone",
        "celular",
        "fixo",
        "número de contato",
        "linha de emergência",
        "número gratuito",
        "ramal",
        "linha direta",
        "linha de atendimento",
        "número de acesso",

        # greek
        "αριθμός τηλεφώνου",
        "κινητό τηλέφωνο",
        "τηλέφωνο",
        "σταθερό",
        "επικοινωνία",
        "σταθερό τηλέφωνο",
        "αριθμός επαφής",
        "αριθμός έκτακτης ανάγκης",
        "δωρεάν αριθμός",
        "παράταση",
        "τηλεφωνική γραμμή",
        "γραμμή βοήθειας",
        "αριθμός πρόσβασης",

        # chinese
        "电话号码",
        "手机号码",
        "固定电话",
        "联系电话",
        "紧急电话",
        "免费电话",
        "分机号",
        "热线电话",
        "服务电话",
        "接入号码",

        # japanese
        "電話番号",
        "携帯電話番号",
        "固定電話",
        "連絡先",
        "緊急電話番号",
        "フリーダイヤル",
        "内線番号",
        "ホットライン",
        "サービスセンター",
        "アクセス番号",

        # french
        "téléphone",
        "téléphonique",
        "portable",
        "numéro de téléphone",
        "numéro de portable",
        "téléphone fixe",
        "numéro de contact",
        "numéro d'urgence",
        "numéro gratuit",
        "poste téléphonique",
        "ligne directe",
        "service client",
        "numéro d'accès",

        # italian
        "telefono",
        "cellulare",
        "fisso",
        "contatto",
        "numero di telefono",
        "numero di cellulare",
        "numero fisso",
        "numero di contatto",
        "numero di emergenza",
        "numero verde",
        "prolunga",
        "linea diretta",
        "servizio clienti",
        "numero di accesso",
    ]
    DEFAULT_SUPPORTED_REGIONS = ("US", "UK", "DE", "FE", "IL", "IN", "CA", "BR")

    def __init__(
        self,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        # For all regions, use phonenumbers.SUPPORTED_REGIONS
        supported_regions=DEFAULT_SUPPORTED_REGIONS, #phonenumbers.SUPPORTED_REGIONS,
        leniency: Optional[int] = 1,
    ):
        context = context if context else self.CONTEXT
        self.supported_regions = supported_regions
        self.leniency = leniency
        super().__init__(
            supported_entities=self.get_supported_entities(),
            supported_language=supported_language,
            context=context,
        )

    def load(self) -> None:  # noqa D102
        pass

    def get_supported_entities(self):  # noqa D102
        return ["PHONE_NUMBER"]

    def analyze(
        self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts = None
    ) -> List[RecognizerResult]:
        """Analyzes text to detect phone numbers using python-phonenumbers.

        Iterates over entities, fetching regions, then matching regional
        phone numbers patterns against the text.
        :param text: Text to be analyzed
        :param entities: Entities this recognizer can detect
        :param nlp_artifacts: Additional metadata from the NLP engine
        :return: List of phone numbers RecognizerResults
        """
        results = []
        for region in self.supported_regions:
            for match in phonenumbers.PhoneNumberMatcher(
                text, region, leniency=self.leniency
            ):
                try:
                    parsed_number = phonenumbers.parse(text[match.start:match.end])
                    region = phonenumbers.region_code_for_number(parsed_number)
                    results += [
                    self._get_recognizer_result(match, text, region, nlp_artifacts)
                ]
                except NumberParseException:
                    results += [
                        self._get_recognizer_result(match, text, region, nlp_artifacts)
                    ]

        return EntityRecognizer.remove_duplicates(results)

    def _get_recognizer_result(self, match, text, region, nlp_artifacts):
        result = RecognizerResult(
            entity_type="PHONE_NUMBER",
            start=match.start,
            end=match.end,
            score=self.SCORE,
            analysis_explanation=self._get_analysis_explanation(region),
            recognition_metadata={
                RecognizerResult.RECOGNIZER_NAME_KEY: self.name,
                RecognizerResult.RECOGNIZER_IDENTIFIER_KEY: self.id,
            },
        )

        return result

    def _get_analysis_explanation(self, region):
        return AnalysisExplanation(
            recognizer=PhoneRecognizer.__name__,
            original_score=self.SCORE,
            textual_explanation=f"Recognized as {region} region phone number, "
            f"using PhoneRecognizer",
        )
