from typing import Generator
import re
import requests

from lxml import etree

from amino import Maybe, List, Nil, Lists, Boolean, Regex, Try, Just
from amino.do import tdo


sanitize_re = re.compile('[._ ]')
url_re = Regex('/(?P<hash>[^/.]+).torrent')
size_re = Regex('(?P<num>[\d.]+) (?P<prefix>[MG])B')


def magnet(hash: str) -> str:
    return f'magnet:?xt=urn:btih:{hash}'


@tdo(Maybe[int])
def parse_size(size_str: str) -> Generator:
    match = yield size_re.match(size_str).to_maybe
    num = yield match.group('num').to_maybe
    prefix = yield match.group('prefix').to_maybe
    mult = 1e6 if prefix == 'M' else 1e9
    num_i = yield Try(float, num).to_maybe
    yield Just(num_i * mult)


def sanitize_query(query: str) -> str:
    return sanitize_re.sub('-', query)


def sub(element: etree.Element, expr: str) -> List[etree.Element]:
    return Lists.wrap(element.xpath(f'descendant::{expr}'))


def text(element: etree.Element, expr: str) -> Maybe[str]:
    return sub(element, expr) // (lambda a: Maybe.optional(a.text))
    return dict(
        title='',
        size=1,
        size_str='1',
        seeders=5,
        magnet_link='',
    )


def cell_texts(row: etree.Element) -> List[str]:
    return Lists.wrap(sub(row, 'td')) // (lambda a: Lists.wrap(a.itertext()))


@tdo(Maybe[dict])
def parse_row(row: etree.Element) -> Generator:
    texts = cell_texts(row)
    title = yield texts.head
    size_str, seeders_str = yield texts.lift_all(-3, -2)
    link = yield sub(row, 'div[@class="tt-name"]/a').head
    url = yield Maybe.optional(link.get('href'))
    hash_match = yield url_re.search(url).to_maybe
    hash = yield hash_match.group('hash').to_maybe
    size = yield parse_size(size_str)
    seeders = yield Try(int, seeders_str.replace(',', '')).to_maybe
    yield Just(dict(
        title=title,
        size=size,
        size_str=size_str,
        seeders=seeders,
        magnet_link=magnet(hash),
    ))


def has_6_cells(row: etree.Element) -> Boolean:
    return Lists.wrap(row.iterchildren()).length == 6


def parse_table(table: etree.Element) -> List[dict]:
    return sub(table, 'tr').filter(has_6_cells) // parse_row


def parse_content(content: etree.Element) -> List[dict]:
    return sub(content, 'table') // parse_table


@tdo(Maybe[List[dict]])
def parse(tree: etree.Element) -> Generator:
    content = yield Lists.wrap(tree.xpath('//*[@id="content"]')).head
    yield Just(parse_content(content))


def search(query: str, category: str='all') -> List[dict]:
    url = f'https://www.limetorrents.cc/search/{category}/{sanitize_query(query)}/seeds/1/'
    html = requests.get(url).content
    tree = etree.fromstring(html, etree.HTMLParser())
    return parse(tree) | Nil


__all__ = ('search',)
