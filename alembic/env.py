import os
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.models import Base

config = context.config
url = os.getenv("DATABASE_URL")
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        {**config.get_section(config.config_ini_section), "sqlalchemy.url": url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

# keep offline/online switch same



if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
