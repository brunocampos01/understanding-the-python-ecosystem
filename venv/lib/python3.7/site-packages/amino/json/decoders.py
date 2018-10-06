from typing import Type, TypeVar, Collection
from numbers import Number

from amino.json.decoder import Decoder, decode
from amino import Maybe, Either, List, Lists, Left
from amino.json.data import JsonError, Json

A = TypeVar('A')


class StringDecoder(Decoder, tpe=str):

    def decode(self, tpe: Type[str], data: Json) -> Either[JsonError, str]:
        return data.scalar.e(f'invalid type for `str`: {data}', data.data)


class NumberDecoder(Decoder, sub=Number):

    def decode(self, tpe: Type[int], data: Json) -> Either[JsonError, int]:
        return data.scalar.e(f'invalid type for `int`: {data}', data.data)


class ListDecoder(Decoder, sub=Collection):

    def decode(self, tpe: Type[Collection], data: Json) -> Either[JsonError, List[A]]:
        def dec() -> Either[JsonError, List[A]]:
            return Lists.wrap(data.data).traverse(decode, Either)
        return data.array.c(dec, lambda: Left(f'invalid type for `List`: {data}'))


class MaybeDecoder(Decoder, tpe=Maybe):

    def decode(self, tpe: Type[Maybe], data: Json) -> Either[JsonError, Maybe]:
        return data.scalar.e(f'invalid type for `Maybe`: {data}', Maybe.check(data.data))

__all__ = ('MaybeDecoder',)
