from typing import Tuple, Generator, Any

from amino import List, Map, Lists, _, Regex, Either, Right, Left, Id, Path
from amino.state import EitherState, State
from amino.regex import Match
from amino.do import tdo
from amino.util.numeric import parse_int

Files = Map[Path, List[str]]
Entry = Map[str, Any]
excludes = List(Regex('In module imported'), Regex('__coconut__'))
error_rex = Regex('(?P<path>[^:]*):(?P<lnum>\d+)(:(?P<col>\d+))?: (error|note): (?P<error>.*)')
lnum_rex = Regex('# line (?P<lnum>\d+)')


@tdo(Either[str, Tuple[str, int, Either[str, int], str]])
def extract(match: Match) -> Generator:
    path = yield match.group('path')
    lnum = yield match.group('lnum')
    lnum_i = yield parse_int(lnum)
    col = match.group('col') // parse_int
    error = yield match.group('error')
    yield Right((Path(path), lnum_i, col, error))


def update_for(path: Path, files: Files) -> Files:
    return files if path in files else files + (path, Lists.lines(path.read_text()))


@tdo(Either[str, Entry])
def substitute(files: Files, path: Path, lnum: int, col: Either[str, int], error: str, coco_path: Path) -> Generator:
    lines = yield files.lift(path).to_either('corrupt state')
    line = yield lines.lift(lnum - 1).to_either(f'invalid line number {lnum} for {path}')
    lnum_match = yield lnum_rex.search(line)
    coco_lnum = yield lnum_match.group('lnum')
    coco_lnum_i = yield parse_int(coco_lnum)
    col_map = col / (lambda a: Map(col=a)) | Map()
    yield Right(Map(lnum=coco_lnum_i, text=error, valid=1, maker_name='mypy') ** col_map)


@tdo(EitherState[Files, Entry])
def handle_coco(path: Path, lnum: int, col: Either[str, int], error: str, coco_path: Path) -> Generator:
    yield EitherState.modify(lambda s: update_for(path, s))
    files = yield EitherState.get()
    yield EitherState.lift(substitute(files, path, lnum, col, error, coco_path))


@tdo(EitherState[Files, Entry])
def line(l: str) -> Generator:
    r = excludes.traverse(lambda a: a.search(l).swap, Either)
    yield EitherState.lift(r)
    match = yield EitherState.lift(error_rex.match(l))
    path, lnum, col, error = yield EitherState.lift(extract(match))
    coco_path = path.with_suffix('.coco')
    yield (
        handle_coco(path, lnum, col, error, coco_path)
        if coco_path.exists() else
        EitherState.failed('not a coconut')
    )


def recover(est: EitherState[Files, Entry]) -> State[Map, Either[str, Entry]]:
    def fix(s: Map, r: Map) -> Id[Tuple[Map, Either[str, Map]]]:
        return Id((s, Right(r)))
    return State.apply(lambda s: est.run(s).map2(fix).value_or(lambda err: Id((s, Left(err)))))


def process_output(output: list) -> List[str]:
    s, result = Lists.wrap(output).map(line).traverse(recover, State).run(Map()).value
    return result.flat_map(_.to_list)

__all__ = ('process_output',)
