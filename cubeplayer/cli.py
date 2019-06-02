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


def duration_type(value: str):
    multiplier = 1
    if value.endswith("ms"):
        multiplier = 0.001
        value = value[:-2]
    elif value.endswith("s"):
        value = value[:-1]
    try:
        val = float(value)
        if val < 0:
            raise ArgumentTypeError("duration cannot be a negative number")
        return val * multiplier
    except ValueError:
        raise ArgumentTypeError(f"invalid number: '{value}'")
