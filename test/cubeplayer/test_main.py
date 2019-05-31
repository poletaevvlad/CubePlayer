from cli.options import truncate_string_around
import pytest


@pytest.mark.parametrize("value, column, out_value, out_column", [
    ("abcde", 3, "abcde", 3),
    ("abcdefghi", 3, "abcdef~~", 3),
    ("abcdefghi", 6, "~~defghi", 5),
    ("abcdefghijklmn", 6, "~~defghi~~", 5)
])
def test_error_message(value: str, column: int, out_value: str, out_column: int) -> None:
    real_value, real_column = truncate_string_around(value, column, 5, 4, "~~")
    assert real_value == out_value
    assert real_column == out_column
