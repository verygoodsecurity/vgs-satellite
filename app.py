import locale
import logging
import os
from multiprocessing import set_start_method

import click

from tblib import pickling_support

from satellite import db
from satellite import logging as satellite_logging
from satellite.aliases.store import AliasStore
from satellite.config import (
    InvalidConfigError,
    SatelliteConfig,
    configure,
    init_satellite_dir,
)
from satellite.routes.loaders import LoadError, load_from_yaml
from satellite.web_application import WebApplication


DEFAULT_CONFIG = SatelliteConfig()


# Do not put default values for non-flag options. Otherwise other config
# sources (env and config file) will be ignored.
@click.command()
@click.option(
    '--debug',
    is_flag=True,
    default=None,
    envvar='SATELLITE_DEBUG',
    help=f'[env:SATELLITE_DEBUG] (default:{DEFAULT_CONFIG.debug}) Debug mode.'
)
@click.option(
    '--web-server-port',  # TODO: Rename to --api-port
    type=int,
    envvar='SATELLITE_API_PORT',
    help=f'[env:SATELLITE_API_PORT] (default:{DEFAULT_CONFIG.web_server_port}) API port. ',
)
@click.option(
    '--reverse-proxy-port',
    type=int,
    envvar='SATELLITE_REVERSE_PROXY_PORT',
    help=(
        '[env:SATELLITE_REVERSE_PROXY_PORT] '
        f'(default: {DEFAULT_CONFIG.reverse_proxy_port}) Reverse proxy port.'
    ),
)
@click.option(
    '--forward-proxy-port',
    type=int,
    envvar='SATELLITE_FORWARD_PROXY_PORT',
    help=(
        '[env:SATELLITE_FORWARD_PROXY_PORT] '
        f'(default:{DEFAULT_CONFIG.forward_proxy_port}) Forward proxy port.'
    ),
)
@click.option(
    '--config-path',
    type=click.Path(exists=True, dir_okay=False),
    envvar='SATELLITE_CONFIG_PATH',
    help=(
        '[env:SATELLITE_CONFIG_PATH] (default:$HOME/.vgs-satellite/config.yml) '
        'Path to the config YAML file.'
    ),
)
@click.option(
    '--db-path',
    type=click.Path(dir_okay=False),
    envvar='SATELLITE_DB_PATH',
    help=(
        '[env:SATELLITE_DB_PATH] (default:$HOME/.vgs-satellite/db.sqlite) '
        'Path to the DB file.'
    ),
)
@click.option(
    '--log-path',
    type=click.Path(dir_okay=False),
    envvar='SATELLITE_LOG_PATH',
    help=('[env:SATELLITE_LOG_PATH] (default:None) Path to a log file.'),
)
@click.option(
    '--silent',
    is_flag=True,
    default=None,
    envvar='SATELLITE_SILENT',
    help=(
        f'[env:SATELLITE_SILENT] (default:{DEFAULT_CONFIG.silent}) '
        'Do not log into stdout.'
    ),
)
@click.option(
    '--volatile-aliases-ttl',
    type=int,
    default=None,
    envvar='VOLATILE_ALIASES_TTL',
    help=(
        f'[env:VOLATILE_ALIASES_TTL] (default:{DEFAULT_CONFIG.volatile_aliases_ttl}) '
        'TTL for volatile aliases in seconds.'
    ),
)
@click.option(
    '--routes-path',
    type=click.Path(exists=True, dir_okay=False),
    envvar='SATELLITE_ROUTES_PATH',
    help=(
        '[env:SATELLITE_ROUTES_PATH] (default:None) Path to a routes config '
        'YAML file. If provided all the current  routes present in Satellite '
        'DB will be deleted.'
    ),

)
def main(**kwargs):
    set_start_method('fork')  # PyInstaller supports only fork start method

    pickling_support.install()

    init_satellite_dir()

    try:
        config = configure(**{
            name: value
            for name, value in kwargs.items()
            if value is not None
        })
    except InvalidConfigError as exc:
        raise click.ClickException(f'Invalid config: {exc}') from exc

    satellite_logging.configure(log_path=config.log_path, silent=config.silent)
    logger = logging.getLogger()

    db.configure(config.db_path)
    try:
        db.init()
    except db.DBVersionMismatch as exc:
        raise click.ClickException(exc) from exc

    if config.routes_path:
        with open(config.routes_path, 'r') as stream:
            try:
                loaded_routes_count = load_from_yaml(stream)
            except LoadError as exc:
                raise click.ClickException(
                    f'Unable to load routes from file: {exc}'
                ) from exc
        logger.info(f'Loaded {loaded_routes_count} routes from routes config file.')

    deleted_aliases = AliasStore.cleanup()
    logger.info(f'Deleted {deleted_aliases} expired aliases.')

    app = WebApplication(config)
    app.start()


if __name__ == '__main__':
    # Locale should be set before runing Click
    lang, encoding = locale.getdefaultlocale()
    if not lang or not encoding:
        os.environ['LC_ALL'] = 'en_US.utf-8'
    main()
