from golgi.config.options import BoolConfigOption

metadata = dict(parents=['series.store_episode', 'series.subsync',
                         'tek_utils.extract'])


def reset_config():
    archive_ext = '(rar|zip|7z|tar\.[bg]z2?)'
    episode_ext = '(mkv|avi|srt)'
    return {
        'handle_episode': dict(
            pretend=False, archive_ext=archive_ext, episode_ext=episode_ext,
            subtitles=BoolConfigOption(True, no=True)
        )
    }
