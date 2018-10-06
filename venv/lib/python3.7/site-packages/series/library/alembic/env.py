from alembic import context
from sqlalchemy import engine_from_config, pool

config = context.config

from series.library.db import FileDatabase
target_metadata = FileDatabase.Base.metadata

import os
from golgi.config import ConfigClient
from series.library.config import reset_config

if not config.get_main_option('sqlalchemy.url'):
    reset_config()
    libd_config = ConfigClient('library')
    db_path = os.environ.get('ALEMBIC_DB', libd_config('db_path'))
    db_url = 'sqlite:///{}'.format(db_path)
    config.set_main_option('sqlalchemy.url', db_url)

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(
                config.get_section(config.config_ini_section),
                prefix='sqlalchemy.',
                poolclass=pool.NullPool)

    connection = engine.connect()
    context.configure(
                connection=connection,
                target_metadata=target_metadata
                )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

