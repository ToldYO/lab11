import pytest

from presidio_anonymizer.operators.initial import Initial


def test_correct_name():
    assert Initial().operator_name() == "initial"


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("John Smith", "J. S."),
        ("john smith", "J. S."),  # lowercase -> uppercase initials
        ("     Eastern    Michigan   University ", "E. M. U."),  # trim & collapse whitespace
        ("@abc", "@A."),  # preserve leading non-alnum prefix
        ("@843A", "@8."),  # first alnum is digit
        ("--**abc", "--**A."),  # preserve prefix
        ("NoAlnum !!! ###", "N. !!! ###"),  # tokens without alnum are kept; token with alnum handled
        ("", ""),  # empty input -> empty output
        (None, None),  # None stays None
    ],
)
def test_given_value_for_initial(input_text, expected):
    result = Initial().operate(input_text)
    assert result == expected
