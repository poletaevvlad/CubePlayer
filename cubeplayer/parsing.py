from typing import List, Tuple

from libcube.actions import Action
from libcube.parser import ParsingError, parse_actions

import click


def construct_error_message(value: str, column: int, left_offset: int = 20, right_offset: int = 20,
                            truncation: str = "...") -> Tuple[str, int]:
    assert len(truncation) < left_offset
    assert len(truncation) < right_offset

    if column > left_offset:
        value = truncation + value[column - left_offset + len(truncation):]
        column = left_offset

    if len(value) - column > right_offset:
        value = value[:column + right_offset - len(truncation) + 1] + truncation

    return value, column


class CubeFormulaParamType(click.ParamType):
    name = "formula"

    def convert(self, value: str, param: str, ctx: click.Context) -> List[Action]:
        try:
            return list(parse_actions(value))
        except ParsingError as e:
            value = value.replace("\n", " ").replace("\t", " ")
            column = e.column
            value, column = construct_error_message(value, column)
            self.fail("".join([str(e), "\n", " " * 7, value, "\n", " " * (7 + column), "^"]), param, ctx)