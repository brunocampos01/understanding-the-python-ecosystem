import os

from golgi.config import (Config, PathConfigOption, ListConfigOption,
                          FileSizeConfigOption, FloatConfigOption,
                          BoolConfigOption, IntConfigOption)

metadata = dict(parents=['series.store_episode', 'series.subsync',
                         'series.etvdb'])


def reset_config():
    day_s = 3600 * 24
    path_template = '{name}/s{season}/{name}_{season:0>2}x{episode:0>2}.{ext}'
    lib_help = 'Add new releases to the library via REST API'
    run_help = ('Comma-separated list of components to start (feed_poller, ' +
                'downloader, archiver, subsyncer, rest_api, link_handler)')
    omit_help = 'List of components not to start'
    Config.override('store_episode', match_threshold=1., overwrite=True)
    return {
        'get': dict(
            rss_urls=ListConfigOption(),
            rss_interval=15 * 60,
            download_dir=PathConfigOption(os.getcwd()),
            run=ListConfigOption([], help=run_help),
            omit=ListConfigOption([], help=omit_help),
            use_sharehosters=True,
            min_size=FileSizeConfigOption(),
            path_template=path_template,
            rest_api_port=8110,
            rest_api_host='0.0.0.0',
            prefer_hosters=ListConfigOption(
                help='hoster domains to prefer with multiple links'),
            subtitle_retry_coefficient=FloatConfigOption(
                30, help='Initial number of minutes to wait before retrying '
                'subtitle downloads'
            ),
            library=BoolConfigOption(True, help=lib_help),
            archive_exec='',
            archive_exec_args='',
            auto_upgrade_db=True,
            link_check_procs=5,
            link_check_proc_timeout=IntConfigOption(
                30, help='timeout for link checking subprocesses in seconds'),
            sync_link_check=False,
            link_check_retry_coefficient=FloatConfigOption(
                5, help='Initial number of minutes to wait before retrying '
                'link checks'
            ),
            db_path=PathConfigOption(),
            sub_exclude=ListConfigOption([]),
            torrent_recheck_interval=3600,
            only_torrent=True,
            full_hd=True,
            min_seeders=0,
            status_new_interval=5,
            download_timeout=60,
            max_size=3.0,
        ),
        'show_planner': dict(
            check_interval=day_s,
            show_db='etvdb'
        ),
        'get_client': dict(
            rest_api_url='http://localhost',
            rest_api_port=8110,
            query_etvdb=True,
        )
    }
