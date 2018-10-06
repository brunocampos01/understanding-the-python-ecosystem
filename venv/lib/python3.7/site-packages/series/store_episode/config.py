from golgi.config import ListConfigOption

metadata = dict(parents=['series'])


def reset_config():
    return {
        'store_episode': dict(
            episodes=ListConfigOption(),
            season_regex='s(\d+)',
            pretend=False,
            remove_prefixes=ListConfigOption(),
            series_name=None,
            season_name=None,
            match_threshold=0.7,
            overwrite=False,
            ask_series=True,
            auto_choose_new_series=False,
        )
    }
