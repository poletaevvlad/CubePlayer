from argparse import ArgumentTypeError


def integer_type(min_value: int):
    def type(value: str):
        try:
            val = int(value)
            if val < min_value:
                raise ArgumentTypeError(f"the minimum value is {min_value}")
            return val
        except ValueError:
            raise ArgumentTypeError(f"invalid int value: '{value}'")
    return type
