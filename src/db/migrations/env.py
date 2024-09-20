from logging.config import fileConfig

import sqlalchemy_utils
from alembic import context
from lib.config import DB_CHARSET, env
from sqlalchemy import create_engine, engine_from_config, pool, text
from sqlalchemy.exc import InternalError, OperationalError
from src.model import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

db_host = env.DB_HOST
db_user = env.DB_USER
db_password = env.DB_PASSWORD
db_name = env.DB_NAME
db_charset = DB_CHARSET

CONNECT_DB_URL = (
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/?charset={db_charset}"
)
DB_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}?charset={db_charset}"

config.set_main_option("sqlalchemy.url", DB_URL)


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    if type_ == "type" and isinstance(obj, sqlalchemy_utils.types.uuid.UUIDType):
        autogen_context.imports.add("import sqlalchemy_utils")
        autogen_context.imports.add("import uuid")
        return "sqlalchemy_utils.types.uuid.UUIDType(binary=False)\
            , default=uuid.uuid4"

    return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def database_exists() -> bool:
    """Check if the database exists."""
    engine = create_engine(DB_URL)
    try:
        engine.connect()
        return True
    except (InternalError, OperationalError) as e:
        print(e)
        return False


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    if not database_exists():
        root = create_engine(CONNECT_DB_URL)
        with root.connect() as conn:
            conn.execute(text(f"CREATE DATABASE {db_name}"))

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
