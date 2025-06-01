import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load variables from .env (including DATABASE_URL)
load_dotenv()

# Alembic Config object
config = context.config

# Sets the database URL (overrides the one in alembic.ini)
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Enable logging as per alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your project metadata so Alembic can recognize the models
from app.models.base import Base
from app.models import user  # importa modelos para incluir nas migrações

# Set the metadata for autogenerate to work correctly
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Executa migrações no modo offline (gera SQL sem executar)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa migrações conectando-se ao banco."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Performs the correct function depending on the mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
