import re
import random

import requests

from series.logging import Logging
from tek.tools import find, resolve_redirect, repr_params, camelcaseify
from tek.util.decorator import generated_list
from golgi.config import configurable

from tek_utils.sharehoster import accepted_domains
from tek_utils.sharehoster.torrent import is_torrent

from series.get.model.release import ReleaseFactory
from series.util import domain


def _valid_entry(entry):
    return ('content' in entry and entry['content'] and
            'value' in entry['content'][0])


class FeedEntry(Logging):

    def __init__(self, release, links=None, is_nuke=False):
        self.release = release
        self.links = links or []
        self.is_nuke = is_nuke

    def __repr__(self):
        params = repr_params(self.release, self.links, self.is_nuke)
        return '{}{}'.format(self.__class__.__name__, params)

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, str(self.release))

    def resolve_redirects(self):
        for i, link in enumerate(self.links):
            if not is_torrent(link):
                try:
                    self.links[i] = resolve_redirect(link)
                except requests.RequestException as e:
                    self.log.error('FeedEntry: {}'.format(e))

    @property
    def is_fix(self):
        return self.release.is_fix


class LinkFinder(object):
    fallback_template = ('{{}} {provider}[^<]+?<a[^>]*?href="(?P<link>[^"]+)"')
    re_template = ''

    def __init__(self, provider):
        self._provider = provider

    def process(self, entry, title):
        if _valid_entry(entry):
            return (self.source_specific(entry, title) or
                    self.fallback(entry, title))

    def source_specific(self, entry, title):
        if self.re_template:
            content = entry['content'][0]['value']
            m = re.search(self.regex(title), content, re.DOTALL | re.I)
            if m:
                return m.group('link')

    def fallback(self, entry, title):
        m = re.search(self.fallback_regex(title),
                      entry['summary_detail']['value'], re.DOTALL | re.I)
        if m:
            return m.group('link')

    def regex(self, title):
        return self.re_template.format(title=title, provider=self._provider)

    def fallback_regex(self, title):
        return self.fallback_template.format(title=title,
                                             provider=self._provider)


class WrzkoLinkFinder(LinkFinder):
    re_template = ('<strong>{title}.+?{provider}.+?<a[^>]*?href=' +
                   '"(?P<link>[^"]+)"')


class RlsbbLinkFinder(LinkFinder):
    re_template = '<strong>{title}.+?<a[^>]*?href="(?P<link>[^"]+)">{provider}'


class FeedTorrentFinder(object):

    def process(self, entry, title):
        link = entry.get('magneturi', entry.get('link'))
        if is_torrent(link):
            return link


class EntryParserMeta(type):

    def __init__(cls, name, bases, dct):
        date_enum = cls.re_separator.join([r'\d{4}', r'\d{2}', r'\d{2}'])
        parts = (cls.re_parts_pre + [cls.enum.format(date=date_enum)] +
                 cls.re_parts_post)
        rex = cls.re_separator.join(parts)
        cls.release_re_raw = r'{}{}'.format(rex, cls.group)
        cls.release_re = re.compile('^{}$'.format(cls.release_re_raw), re.I)
        super(EntryParserMeta, cls).__init__(name, bases, dct)


class EntryParser(object, metaclass=EntryParserMeta):
    _name = r'(?P<name>.+?)'
    enum = r'(?P<enum>S?\d{{1,2}}?[xE]\d{{1,2}}?|{date})((-|E)\d{{1,2}}?)?'
    _flags = r'(?P<flags>.+?)?'
    group = r'(-(?P<group>[^-]+?))?'
    re_parts_pre = [_name]
    re_parts_post = [_flags]
    re_separator = '\.'
    domain = ''
    _release_fact = ReleaseFactory()

    def __init__(self, entry, link_finders):
        self.entry = entry
        self._link_finders = link_finders
        self._releases = None

    @property
    def valid(self):
        return self.release is not None

    @property
    def release(self):
        return find(lambda r: r.hd_series, self.releases)

    @property
    def title(self):
        return self.release.title if self.release else ''

    @property
    def titles(self):
        return [self.entry['title']]

    @property
    def releases(self):
        if self._releases is None:
            self._releases = self._find_releases()
        return self._releases

    def _find_releases(self):
        return self._releases_from_titles()

    @property
    def links(self):
        return [_f for _f in [self._find_link(finder) for finder in
                              self._link_finders] if _f]

    def _find_link(self, finder):
        return finder.process(self.entry, self.title)

    @generated_list
    def _releases_from_titles(self):
        for title in self.titles:
            release = self._release_from_title(title)
            if release:
                yield release

    def _release_from_title(self, title):
        title = title.lower().strip()
        match = self.release_re.match(title)
        if match:
            return self._release_fact.from_title_match(title, match)
        else:
            text = 'Couldn\'t match title "{}"'.format(title)
            self.log.error(text)


class WrzkoParser(EntryParser):
    domain = 'wrzko'

    @property
    def titles(self):
        return [t.lower().strip() for t in self.entry['title'].split('&')]


class RlsbbParser(EntryParser):
    domain = 'rlsbb'

    @property
    def titles(self):
        title_re = '<strong> *({}) *<'.format(self.release_re_raw)
        if _valid_entry(self.entry):
            content = self.entry['content'][0].value
            candidates = re.findall(title_re, content)
            return [c[0].lower().strip() for c in candidates if c]
        else:
            return []


class EzrssParser(EntryParser):
    domain = 'ezrss'

    @property
    def titles(self):
        title = self.entry.get('filename', '').rsplit('.', 2)[0]
        return [title]


class ShowrssParser(EntryParser):
    domain = 'showrss'

    @property
    def titles(self):
        title = self.entry.get('showrss_rawtitle', '').replace(' ', '.')
        title = '-'.join(title.rsplit('.', 1))
        return [title]


@configurable(general=['verbose'])
class FeedEntryFactory(Logging):

    def __init__(self, rss_url):
        self.domain = domain(rss_url)
        self._Parser = globals().get(
            camelcaseify('{}_parser'.format(self.domain)), EntryParser
        )
        _LinkFinder = globals().get(
            camelcaseify('{}_link_finder'.format(self.domain)), LinkFinder)
        self._link_finders = [_LinkFinder(p) for p in accepted_domains()]
        self._link_finders += [FeedTorrentFinder()]

    def process_items(self, items, want_hd=True):
        entries = [self.process_item(item, want_hd) for item in items]
        return [e for e in entries if e is not None]

    def process_item(self, item, want_hd=True):
        parser = self._Parser(item, self._link_finders)
        if parser.valid:
            return FeedEntry(parser.release, links=parser.links)
        else:
            if self._verbose:
                msg = 'Discarding feed entry "{}" with releases:'
                self.log.warning(msg.format(item['title']))
                for release in parser.releases:
                    self.log.warning(release)

    def from_title(self, title, want_hd=True):
        return self.process_item(dict(title=title), want_hd)


class FeedEntryHasher(object):

    def __init__(self, rss_url):
        pass

    def __call__(self, entry):
        if _valid_entry(entry):
            return hash(tuple(entry['content'][0]['value']))
        else:
            return random.randint(0, 1000000)
