from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI

from ..core.config import settings


# lifespan function to manage the database connection pool
@asynccontextmanager
async def lifespan(app: FastAPI):
    # create the connection pool
    print("Starting up: Creating database connection pool...")

    app.state.db_pool = await asyncpg.create_pool(settings.database_url)

    # the api runs while this is yielding
    yield

    # close the connection pool
    print("Shutting down: Closing database connection pool...")

    await app.state.db_pool.close()
