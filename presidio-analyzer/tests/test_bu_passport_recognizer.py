import pytest

from tests import assert_result_within_score_range
from presidio_analyzer.predefined_recognizers import BuPassportRecognizer


@pytest.fixture(scope="module")
def recognizer():
    return BuPassportRecognizer()


@pytest.fixture(scope="module")
def entities():
    return ["BU_PASSPORT_NUMBER"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions, expected_score_ranges",
    [
        # fmt: off
        ("487290948", 1, ((0, 9),), ((0.0, 0.1),),),
        ("744198477", 1, ((0, 9),), ((0.0, 0.1),),),
        # fmt: on
    ],
)
def test_when_passport_in_text_then_all_bu_passports_found(
    text,
    expected_len,
    expected_positions,
    expected_score_ranges,
    recognizer,
    entities,
    max_score,
):
    results = recognizer.analyze(text, entities)
    assert len(results) == expected_len
    for res, (st_pos, fn_pos), (st_score, fn_score) in zip(
        results, expected_positions, expected_score_ranges
    ):
        if fn_score == "max":
            fn_score = max_score
        assert_result_within_score_range(
            res, entities[0], st_pos, fn_pos, st_score, fn_score
        )