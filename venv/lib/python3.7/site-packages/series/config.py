from golgi.config import PathConfigOption, ListConfigOption

metadata = dict(parents=['tek_utils.sharehoster'])


def reset_config():
    return {
        'series': dict(
            series_dir=PathConfigOption(),
            temp_dir=PathConfigOption(),
            monitor=ListConfigOption(),
            library_url='http://localhost:8111',
            enumeration_regex='',
        ),
        'client': dict(cli_cmd=None, cli_params=[],)
    }
