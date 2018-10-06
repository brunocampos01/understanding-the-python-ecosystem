import abc
from typing import TypeVar, Generator, Any, Type, Generic

from amino.tc.base import TypeClass
from amino import Either, Map, Right, Lists
from amino.do import tdo
from amino.json.data import JsonError, JsonObject, JsonArray, JsonScalar, Json
from amino.json.parse import parse_json
from amino.dispatch import dispatch_alg

A = TypeVar('A')


class Decoder(Generic[A], TypeClass):

    @abc.abstractmethod
    def decode(self, tpe: Type[A], data: Map[str, Any]) -> Either[JsonError, A]:
        ...


@tdo(Either[str, A])
def decode_json_object(data: dict) -> Generator:
    m = Map(data)
    tpe_s = yield m.get('__type__').to_either(f'no `__type__` attr in json object {m}')
    tpe = yield Either.import_path(tpe_s)
    dec = yield Decoder.e(tpe)
    yield dec.decode(tpe, m)


class Decode:

    @tdo(Either[str, A])
    def decode_json_object(self, json: JsonObject) -> Either[str, A]:
        tpe = yield json.tpe
        dec = yield Decoder.e(tpe)
        yield dec.decode(tpe, json)

    def decode_json_array(self, json: JsonArray) -> Either[str, A]:
        return Lists.wrap(json.data).traverse(decode, Either)

    def decode_json_scalar(self, json: JsonScalar) -> Either[str, A]:
        return Right(json.data)


decode = dispatch_alg(Decode(), Json, 'decode_')


@tdo(Either[JsonError, A])
def decode_json(data: str) -> Generator:
    json = yield parse_json(data)
    yield decode(json)

__all__ = ('Decoder', 'decode_json_object', 'decode_json')
