from golgi.config import ListConfigOption, DictConfigOption, ConfigOption

metadata = dict(parents=['series'])


def reset_config():
    return {
        'subsync': dict(
            splitchar='|', base_url=None, cookies=DictConfigOption(),
            series_url_map=DictConfigOption(), only_latest=False,
            episodes=ListConfigOption(positional=True),
            cli_dir=ConfigOption(positional=True),
        )
    }
