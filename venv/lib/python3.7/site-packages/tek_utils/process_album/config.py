from golgi.config import ListConfigOption

metadata = dict(parents=['tek_utils.extract', 'mootag.store', 'mootag'])


def reset_config():
    return {
        'process_album': dict(
            music_tempdir='/home/media/new',
            album=ListConfigOption(positional=True)
        )
    }
