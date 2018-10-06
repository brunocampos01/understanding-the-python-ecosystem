from pathlib import Path

from golgi.config import (PathConfigOption, DictConfigOption,
                          ListConfigOption, BoolConfigOption,
                          FileSizeConfigOption, IntConfigOption)


metadata = dict(parents=['tek_utils'], alias='sharehoster')


def reset_config():
    config = {}
    config['sharehoster'] = dict(out_dir=PathConfigOption(Path.cwd()),
                                 link_checker_url=None,
                                 link_check_critical=False,
                                 progress_update_interval=1,
                                 timeout=IntConfigOption(5),
                                 resume=BoolConfigOption(True, no=True),
                                 retry=-1,
                                 )
    config['rapidshare'] = dict(login=None, password=None)
    config['netload'] = dict(cookies=DictConfigOption())
    config['uploaded'] = dict(cookies=DictConfigOption())
    config['zevera'] = dict(user='', password='',
                            providers=ListConfigOption())
    min_size_help = 'Minimum of the file size sum on a single page'
    min_size = FileSizeConfigOption(short='s', help=min_size_help)
    config['search'] = dict(web_url=None,
                            match_url=ListConfigOption([], short='m'),
                            match_url_all=BoolConfigOption(False, short='M'),
                            terms=ListConfigOption(positional=True),
                            min_size=min_size, providers=ListConfigOption())
    config['shget'] = dict(urls=ListConfigOption(positional=True))
    config['tget'] = dict(urls=ListConfigOption(positional=True))
    config['torrent'] = dict(cacher='', limit=9, short='l',
                             delete=BoolConfigOption(False, short='d'),
                             pirate_bay_url='https://thepiratebay.se',
                             search_engine='kickass')
    config['putio'] = dict(token='')
    config['kickass'] = dict(host='kat.al')
    config['piratebay'] = dict(host='thepiratebay.org')
    return config
