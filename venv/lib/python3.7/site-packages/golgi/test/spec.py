from golgi import Config

Config.enable_lazy_class_attr = False


class SpecConfigConcern:

    def setup(self, configs=['golgi'], allow_files=False, *a, **kw):
        Config.allow_files = allow_files
        Config.setup(*configs, files=allow_files)

__all__ = ('SpecConfigConcern',)
