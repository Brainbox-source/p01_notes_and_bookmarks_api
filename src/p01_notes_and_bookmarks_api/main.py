from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI, Request

# import the router
from .api import bookmarks, notes
from .core.config import settings


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


# initialize the FastAPI app with the lifespan
app = FastAPI(lifespan=lifespan)

# register the routers with the main app
app.include_router(notes.router)
app.include_router(bookmarks.router)


# endpoint to verify the database connection
@app.get("/test-db")
async def test_database_connection(request: Request):
    # borrow a connection from the pool
    async with request.app.state.db_pool.acquire() as connection:
        # run a raw sql query
        version = await connection.fetchval("SELECT version();")
        return {"postgres_version": version}
