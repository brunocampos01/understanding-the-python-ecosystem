import abc
import json
from typing import TypeVar, Generator, Generic

from amino.tc.base import TypeClass
from amino import Either, L, _
from amino.do import tdo
from amino.json.data import JsonError, Json

A = TypeVar('A')


class Encoder(Generic[A], TypeClass):

    @abc.abstractmethod
    def encode(self, a: A) -> Either[JsonError, Json]:
        ...


@tdo(Either[JsonError, Json])
def encode_json(data: A) -> Generator:
    enc = yield Encoder.e_for(data).lmap(L(JsonError)(data, _))
    yield enc.encode(data)


def dump_json(data: A) -> Either[JsonError, str]:
    return encode_json(data) / _.native / json.dumps

__all__ = ('Encoder', 'encode_json', 'dump_json')
