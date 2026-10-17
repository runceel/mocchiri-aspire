import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from db import RANKING_CACHE_KEY, cache, connect, create_tables
from telemetry import configure_telemetry

RANKING_CACHE_SECONDS = 30


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時にテーブルを作る（DB がまだ起動していないと、ここで落ちる）
    create_tables()
    yield


app = FastAPI(title="もっちり頒布マネージャー API", lifespan=lifespan)
configure_telemetry(app)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/books")
def list_books():
    with connect() as conn:
        return conn.execute(
            """
            SELECT b.id, b.title, b.price, b.stock, COUNT(s.id) AS sold
            FROM books b
            LEFT JOIN sales s ON s.book_id = b.id
            GROUP BY b.id
            ORDER BY b.id
            """
        ).fetchall()


@app.post("/books/{book_id}/sales")
def sell_book(book_id: int):
    with connect() as conn:
        book = conn.execute(
            "SELECT id, stock FROM books WHERE id = %s FOR UPDATE", (book_id,)
        ).fetchone()
        if book is None:
            raise HTTPException(status_code=404, detail="本が見つかりません")
        if book["stock"] <= 0:
            raise HTTPException(status_code=409, detail="在庫がありません")

        conn.execute("UPDATE books SET stock = stock - 1 WHERE id = %s", (book_id,))
        conn.execute("INSERT INTO sales (book_id) VALUES (%s)", (book_id,))

    # 売れたのでランキングのキャッシュを捨てる
    cache.delete(RANKING_CACHE_KEY)
    return {"id": book_id, "stock": book["stock"] - 1}


@app.get("/ranking")
def ranking():
    cached = cache.get(RANKING_CACHE_KEY)
    if cached is not None:
        return json.loads(cached)

    with connect() as conn:
        rows = conn.execute(
            """
            SELECT b.id, b.title, COUNT(s.id) AS sold
            FROM books b
            JOIN sales s ON s.book_id = b.id
            GROUP BY b.id
            ORDER BY sold DESC, b.id
            LIMIT 5
            """
        ).fetchall()

    cache.set(RANKING_CACHE_KEY, json.dumps(rows), ex=RANKING_CACHE_SECONDS)
    return rows
