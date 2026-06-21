import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.infrastructure.config import settings
from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence import models  # noqa: F401 — registers tables on Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# PostGIS ships system tables (spatial_ref_sys) and, with the full image, the
# Tiger geocoder + topology schemas. We must not let autogenerate try to drop them.
EXCLUDED_SCHEMAS = {"tiger", "tiger_data", "topology"}


def include_object(obj, name, type_, reflected, compare_to):
    if type_ == "table":
        if getattr(obj, "schema", None) in EXCLUDED_SCHEMAS:
            return False
        # Ignore any reflected table that isn't part of our own models.
        if reflected and name not in target_metadata.tables:
            return False
    return True


def _configure(**kw):
    context.configure(
        target_metadata=target_metadata,
        include_object=include_object,
        include_schemas=False,
        **kw,
    )


def run_migrations_offline():
    _configure(url=settings.DATABASE_URL, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(settings.DATABASE_URL)
    async with connectable.connect() as connection:
        await connection.run_sync(lambda conn: _configure(connection=conn))
        async with connection.begin():
            await connection.run_sync(lambda _: context.run_migrations())
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
