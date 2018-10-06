import urllib.error
import re

import feedparser

from xml.sax import SAXException

from series.logging import Logging
from golgi.config import configurable
from tek.tools import find

from series.get.handler import ReleaseHandler
from series.get.model.feed_entry import FeedEntryFactory
from series.get.model.feed_entry import FeedEntryHasher
from series.get.model.release import ReleaseFactory

feedparser.PREFERRED_XML_PARSERS = []


@configurable(series=['monitor'], get=['rss_urls', 'rss_interval'])
class FeedPoller(ReleaseHandler):

    def __init__(self, releases, *a, **kw):
        super().__init__(releases, self._rss_interval,
                                         'feed poller')
        self._rss = None
        self._etags = [None] * len(self._rss_urls)
        self._modified = [None] * len(self._rss_urls)
        self._release_fact = ReleaseFactory()
        self._hashes = set()
        self._feed_entries = []

    def reconstruct_entries(func):
        def wrapper(dl, *a, **kw):
            ret = func(dl, *a, **kw)
            dl._reconstruct_entries()
            return ret
        return wrapper

    @reconstruct_entries
    def load_from_xml_file(self, fname):
        self._rss = feedparser.parse(fname)

    @reconstruct_entries
    def load_from_url(self, url, index):
        try:
            self._rss = feedparser.parse(url, etag=self._etags[index],
                                         modified=self._modified[index])
            self._etags[index] = self._rss.get('etag', None)
            self._modified[index] = self._rss.get('modified_parsed', None)
        except (urllib.error.URLError, urllib.error.HTTPError,
                SAXException) as e:
            self.log.debug(e)

    def _check(self):
        for index, url in enumerate(self._rss_urls):
            self.load_from_url(url, index)

    def _reconstruct_entries(self):
        if self._rss and self._rss.entries:
            hasher = FeedEntryHasher(self._rss.feed.link)
            valid = lambda e: (bool(e) and not hasher(e) in self._hashes)
            valid_entries = list(filter(valid, self._rss.entries))
            self._hashes |= set([hasher(e) for e in valid_entries])
            fact = FeedEntryFactory(self._rss.feed.link)
            self._feed_entries = fact.process_items(reversed(valid_entries))
            text = 'Found {} series entries in the feed "{}".'
            self.log.info(text.format(len(self._feed_entries), fact.domain))
            self._update_monitors()

    def _update_monitors(self):
        for entry in filter(self._is_monitored, self._feed_entries):
            existing = self._find_release(entry)
            if existing is None:
                self._create_monitor(entry)
            else:
                self._releases.add_links_from_feed_entry(existing, entry)

    def _create_monitor(self, entry):
        monitor = self._release_fact.monitor_from_entry(entry)
        old_entry = self._find_nuke(entry)
        if old_entry is not None:
            if not entry.is_fix:
                self._update(monitor, downloaded=old_entry.downloaded)
                self._update(monitor, archived=old_entry.archived)
            old_entry.nuke(monitor)
        self._releases.add(monitor)
        self.log.info('Added monitor for {!s}'.format(monitor.release))

    def _find_release(self, entry):
        return find(lambda m: m.release == entry.release, self._releases.all)

    def _find_nuke(self, entry):
        return find(lambda m: m.release.is_same_episode(entry.release),
                    self._releases.all)

    def _is_monitored(self, entry):
        name = entry.release.name
        if re.search(r'_\d{4}$', name):
            name = name.rsplit('_', 1)[0]
        return name in self._monitor

__all__ = ['FeedPoller']
