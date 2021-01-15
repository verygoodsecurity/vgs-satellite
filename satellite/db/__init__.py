import threading
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from .models import Base


class DBVersionMismatch(Exception):
    pass


def configure(db_path: str):
    global _engine
    global _Session

    _engine = create_engine(f'sqlite:///{db_path}')
    _Session = sessionmaker(bind=_engine)


def get_engine():
    return _engine


def get_session() -> Session:
    if not hasattr(_session_store, 'session'):
        _session_store.session = _Session()
    return _session_store.session


def init():
    alembic_cfg = Config()
    alembic_cfg.set_main_option(
        'script_location',
        str(Path(__file__).parent / 'migrations'),
    )
    try:
        Base.metadata.create_all(_engine, checkfirst=False)
    except OperationalError:
        # DB was initialized before. Applying migrations.
        try:
            command.upgrade(alembic_cfg, 'head')
        except CommandError as exc:
            db_path = str(get_engine().url).replace('sqlite:///', '')
            if str(exc).startswith("Can't locate revision identified by"):
                raise DBVersionMismatch(
                    'Looks like DB version is newer than version of the app. '
                    'Please update the app or reset the DB by removing the '
                    f'DB file ({db_path}) or pointing the app to an another DB '
                    'file path.'
                ) from exc
            raise
    else:
        # We have a fresh DB. Stamping with the latest version.
        command.stamp(alembic_cfg, 'head')

    # If some migrations dropped tables which must be recreated
    Base.metadata.create_all(_engine)


def update_model(model: Base, data: dict, exclude_fields=None):
    for name, value in data.items():
        exclude = exclude_fields and name in exclude_fields
        if not exclude and name in model.__table__.columns:
            setattr(model, name, value)


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


_engine = None
_Session = None
_session_store = threading.local()
