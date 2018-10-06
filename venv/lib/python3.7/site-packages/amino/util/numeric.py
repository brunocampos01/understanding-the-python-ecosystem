import numbers
from typing import Any

from amino import may, Right, Left, Maybe, Either


@may
def try_convert_int(data: Any) -> Maybe[int]:
    if (
            isinstance(data, numbers.Number) or
            (isinstance(data, str) and data.isdigit())
    ):
        return int(data)


def parse_int(i: Any) -> Either[str, int]:
    return Right(i) if isinstance(i, int) else (
        Right(int(i)) if isinstance(i, str) and i.isdigit() else
        Left('could not parse int {}'.format(i))
    )

__all__ = ('try_convert_int', 'parse_int')
