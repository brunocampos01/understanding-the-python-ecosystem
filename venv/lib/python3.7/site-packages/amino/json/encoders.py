from typing import Union, Collection, TypeVar
from numbers import Number

from amino import Either, List, L, _, Right, Lists, Maybe
from amino.json.encoder import Encoder, encode_json
from amino.json.data import JsonError, Json, JsonArray, JsonScalar

A = TypeVar('A')


class ScalarEncoder(Encoder[Union[Number, str, None]], pred=L(issubclass)(_, (Number, str, type(None)))):

    def encode(self, a: Union[Number, str, None]) -> Either[JsonError, Json]:
        return Right(JsonScalar(a))


class ListEncoder(Encoder[List], pred=L(issubclass)(_, Collection)):

    def encode(self, a: Collection) -> Either[JsonError, Json]:
        return Lists.wrap(a).traverse(encode_json, Either) / JsonArray


class MaybeEncoder(Encoder[Maybe], tpe=Maybe):

    def encode(self, a: Maybe[A]) -> Either[JsonError, Json]:
        return Right(JsonScalar(a | None))

__all__ = ('ListEncoder', 'ScalarEncoder')
