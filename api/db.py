import psycopg
import redis
from psycopg.rows import dict_row

from settings import DATABASE_URL, REDIS_URL

RANKING_CACHE_KEY = "ranking"

cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def connect() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def create_tables() -> None:
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                price INTEGER NOT NULL,
                stock INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL REFERENCES books (id),
                sold_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
