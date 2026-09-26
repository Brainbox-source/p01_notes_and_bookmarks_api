from fastapi import FastAPI, Request

from .api import bookmarks, notes  # import the routers
from .api.dependencies import get_db_pool
from .db.database import lifespan

# initialize the FastAPI app with the lifespan
app = FastAPI(lifespan=lifespan)

# register the note and bookmarks routers with the main app
app.include_router(notes.router)
app.include_router(bookmarks.router)


# verify the database connection
@app.get("/")
async def test_database_connection(request: Request):
    """tests the database connection"""

    pool = get_db_pool(request)

    query = """
        SELECT version();
    """

    # borrow a connection from the pool, run the query, and return the connection to the pool
    async with pool.acquire() as connection:
        version = await connection.fetchval(query)

        return {"msg": "Connection Successful! ✅", "postgres_version": version}
