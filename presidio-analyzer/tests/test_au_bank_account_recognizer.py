import pytest

from tests import assert_result_within_score_range
from presidio_analyzer.predefined_recognizers import AuBankAccountRecognizer


@pytest.fixture(scope="module")
def recognizer():
    return AuBankAccountRecognizer()


@pytest.fixture(scope="module")
def entities():
    return ["AU_BANK_ACCOUNT_NUMBER"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions, expected_score_ranges",
    [
        # Medium 
        ("010-010146231", 1, ((0, 13),), ((0.0, 0.4),), ),
        ("010-010 146231", 1, ((0, 14),), ((0.0, 0.4),), ),
        # Weak 
        ("010-12312345", 1, ((0, 12),), ((0.0, 0.3),), ),
        ("528 247 53556", 1, ((0, 13),), ((0.0, 0.3),), ),
        # Invalid  
        ("52824753556AF", 0, (), (),),
        ("51 824 753 5564", 0, (), (),),
        ("123 456\n789", 0, (), (),),
    ],
)
def test_when_all_au_bank_account_number_then_succeed(
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
