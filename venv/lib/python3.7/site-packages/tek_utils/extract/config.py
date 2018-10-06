from golgi.config import Config, ListConfigOption
from golgi.config.options import BoolConfigOption

metadata = dict(parents=['tek_utils'])


def reset_config():
    Config.set_cli_short_options(ask_password='p', global_password='g',
                                 list='l')
    return {
        'extract': dict(
            ask_password=False, passwords=ListConfigOption(), archive=[],
            temp=BoolConfigOption(True, no=True, no_switch='-T'),
            rar_switches=ListConfigOption(), tar_switches=ListConfigOption(),
            global_password=False, password=None, list=False
        )
    }
