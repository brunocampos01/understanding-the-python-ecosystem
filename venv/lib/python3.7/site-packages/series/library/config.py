''' configuration for library '''

from golgi.config import (PathListConfigOption, PathConfigOption,
                        ListConfigOption, FloatConfigOption)
from golgi.config.options import DictConfigOption

metadata = dict(parents=['series.etvdb'])


def reset_config():
    ''' Initialize the config. '''
    season_dir = '{name}/s{season}/'
    episode = '{name}_{season:0>2}x{episode:0>2}.{ext}'
    path_template = season_dir + episode
    subtitle_path_template = season_dir + 'sub/' + episode
    movie_path_template = '{title}.{ext}'
    movie_subtitle_path_template = 'sub/{title}.{ext}'
    run_help = ('Comma-separated list of components to start (rest_api, ' +
                'metadata)')
    omit_help = 'List of components not to start'
    resume_before_help = (
        'Relative value in [0, 1], when an episode has been stopped at a '
        'position before this progress, it is resumed there when starting '
        'again')
    return {
        'library': dict(
            collection_paths=PathListConfigOption(),
            movie_collection_paths=PathListConfigOption(),
            path_template=path_template,
            subtitle_path_template=subtitle_path_template,
            movie_path_template=movie_path_template,
            movie_subtitle_path_template=movie_subtitle_path_template,
            rest_api_port=8111,
            rest_api_host='0.0.0.0',
            db_path=PathConfigOption(),
            name_formatter='',
            run=ListConfigOption([], help=run_help),
            omit=ListConfigOption([], help=omit_help),
            metadata_interval=300,
        ),
        'player': dict(
            display=None,
            path='mplayer2',
            args=DictConfigOption(dict(fs='yes')),
            resume_before=FloatConfigOption(0, help=resume_before_help),
            subtitles=True,
            mplayer_extra_args=DictConfigOption({}),
            mpv_extra_args=DictConfigOption(dict(input_default_bindings='yes',
                                                 input_vo_keyboard='yes')),
            player_type='mplayer',
        ),
        'library_client': dict(
            rest_api_url='http://localhost', rest_api_port=8111
        )
    }

__all__ = ['reset_config', 'metadata']
