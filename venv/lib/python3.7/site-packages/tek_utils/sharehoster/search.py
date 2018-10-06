import re
import itertools
from lxml import etree

import requests

from tek import logger
from golgi import configurable, Config, cli
from golgi.io.terminal import terminal
from tek.tools import decode, parallel_map

from tek_utils.sharehoster.errors import (NoMoreResults, RapidshareError,
                                          InvalidURLError)
from tek_utils.sharehoster import downloader, DownloadChoice, accepted_domains


def normalize(data):
    chars = '[.\- ]+'
    data = data.lower()
    data = data.strip(chars)
    data = re.split(chars, data)
    data = '_'.join(data)
    return data


@configurable(search=['web_url'])
class SearchEngine(object):
    _trim_rex = re.compile('(http://[^&]+)')

    def __init__(self, query, hl='en'):
        self._query = query
        self._hl = hl
        self.__init_attributes()

    def __init_attributes(self):
        self._params = dict(q=self._query.encode('utf-8'), hl=self._hl,
                            oe='utf8', ie='utf8')
        self._headers = dict({'user-agent': 'Mozilla'})

    def _request(self, number, **kw):
        params = dict(self._params)
        params.update(start=str(number*10), **kw)
        return requests.get(self._web_url, params=params,
                            headers=self._headers)

    def search(self, **kw):
        try:
            for i in itertools.count():
                try:
                    data = self._request(i, **kw).content
                    for url in self._extract_urls(data):
                        yield url
                except requests.Timeout:
                    logger.warn('Timeout in search!')
        except (requests.RequestException, NoMoreResults) as e:
            logger.info('Search aborted: {}'.format(e))

    def _extract_urls(self, data):
        tree = etree.fromstring(data, etree.HTMLParser())
        urls = tree.xpath("//h3[@class='r']/child::a/attribute::href")
        urls = [_f for _f in map(self._trim, urls) if _f]
        if not urls:
            raise NoMoreResults()
        return urls

    def _trim(self, url):
        match = self._trim_rex.search(url)
        return match.groups(1)[0] if match else ''


@configurable(search=['match_url', 'match_url_all', 'terms', 'min_size',
                           'providers'])
class SiteValidator(object):

    def __init__(self):
        rexify = lambda rexes: list(map(re.compile, rexes,
                                    itertools.repeat(re.I)))
        self._match_rexes = rexify(self._match_url)
        if self._match_url_all:
            self._match_rexes.extend(rexify(list(map(normalize, self._terms))))

    def valid_link(self, url):
        try:
            return downloader(url)
        except (RapidshareError, requests.RequestException, InvalidURLError):
            return False

    def match_link(self, url):
        url = normalize(url)
        matches = [rex.search(url) for rex in self._match_rexes]
        return not self._match_rexes or (all(matches) and bool(matches))

    def valid_sites(self, sites):
        nonurl = '[^ <"\'\n]+'
        provider_or = '|'.join(accepted_domains())
        rex = r'(https?://(?:{})\.{})'.format(provider_or, nonurl)
        filename = lambda u: u.split('/')[-1]
        for url, content in sites:
            links = re.findall(rex, content)
            links = sorted(set(links), key=filename)
            valid_links = list(filter(self.match_link, links))
            downloaders = parallel_map(self.valid_link, valid_links)
            valid_downloaders = [_f for _f in downloaders if _f]
            total_size = sum((l.file_size for l in valid_downloaders))
            if valid_downloaders and (self._min_size == -1 or total_size >
                                      self._min_size):
                yield url, valid_downloaders


@configurable(search=['providers'])
class ReleaseCrawler(object):

    def __init__(self, release):
        self._release = release

    def sites(self):
        providers = accepted_domains()
        provider_urls = list(map('"http://{}."'.format, providers))
        provider_or = ' OR '.join(provider_urls)
        query = '{} {}'.format(provider_or, self._release)
        search = SearchEngine(query)
        for url in search.search():
            terminal.write('.')
            terminal.flush()
            try:
                yield url, requests.get(url, timeout=2).text
            except requests.RequestException:
                pass

    def get_release(self):
        validator = SiteValidator()
        for site, links in validator.valid_sites(self.sites()):
            terminal.write_lines(['Found at {}'.format(site), ''])
            dl = DownloadChoice(links)
            if dl.run():
                return


@cli(positional=('terms', '+'))
def sh_release():
    terms = Config['search'].terms
    query = ' '.join(['"{}"'.format(decode(a)) for a in terms])
    crawler = ReleaseCrawler(query)
    crawler.get_release()
