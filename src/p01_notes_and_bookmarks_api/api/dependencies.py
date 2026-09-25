import asyncpg
from fastapi import Request


# dependency to get the database pool
def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool
