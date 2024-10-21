# Standard Library imports
import os
from pathlib import Path
import sys
from logging.config import fileConfig

# Third-party imports
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import dotenv_values

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Load logging configuration if available
#if os.path.exists('logging.conf'):
 #   fileConfig('logging.conf')
#else:
   # print("Warning: logging.conf not found, using default logging configuration.")

# Get db uri depending on argument passed
cmd_kwargs = context.get_x_argument(as_dictionary=True)
if "db" not in cmd_kwargs:
    raise Exception(
        "We couldn't find `db` in the CLI arguments. "
        "Please verify `alembic` was run with `-x db=<db_name>` "
        "(e.g. `alembic -x db=dev upgrade head`)"
    )

db_env = cmd_kwargs["db"]

if db_env not in ["dev", "test"]:
    raise Exception(
        "The `db` argument only accepts `dev` or `test`."
        "Please verify `alembic` was run with `-x db=<db_name>` "
        "(e.g. `alembic -x db=dev upgrade head`)"
    )

def get_dot_env():
    cwd = Path(os.getcwd())
    env_file = Path(cwd, ".flaskenv")
    values = dotenv_values(env_file)
    return values

env_values = get_dot_env()

# Set the SQLAlchemy URL based on the environment
if db_env == "dev":
    config.set_main_option("sqlalchemy.url", env_values["DEV_DATABASE_URI"])
elif db_env == "test":
    config.set_main_option("sqlalchemy.url", env_values["TEST_DATABASE_URI"])

# Adding current working directory to import models
cwd = os.getcwd()
sys.path.append(cwd)

# App imports
from app.models import Base  # Ujisti se, že toto importuje správnou třídu Base

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
