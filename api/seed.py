"""テストデータを投入するスクリプト。

初回は `uv run python seed.py` を実行してください。
今入っているデータは全部消えます。
"""

from db import RANKING_CACHE_KEY, cache, connect, create_tables

# (タイトル, 価格, 在庫, 頒布済みの数)
BOOKS = [
    ("Azure MixBook 23H1", 1000, 6, 4),
    ("Azure MixBook 23H2", 1000, 8, 5),
    ("Azure MixBook 24H1", 1000, 10, 3),
    ("Azure MixBook 24H2", 1000, 12, 7),
    ("Azure MixBook 25H1", 1500, 15, 6),
    ("Azure MixBook 25H2", 1500, 20, 12),
    ("上から下までMicrosoftテクノロジーで作る！ 秘書エージェント", 2000, 15, 9),
    (
        "技術書典に本を出すことになったがパーティーの方針が定まらないまま"
        "皆が好きなことを書いた件について",
        1000,
        5,
        2,
    ),
]


def reset_and_seed_books() -> None:
    create_tables()
    with connect() as conn:
        conn.execute("TRUNCATE sales, books RESTART IDENTITY")
        for title, price, stock, sold in BOOKS:
            book = conn.execute(
                "INSERT INTO books (title, price, stock) VALUES (%s, %s, %s) RETURNING id",
                (title, price, stock),
            ).fetchone()
            for _ in range(sold):
                conn.execute("INSERT INTO sales (book_id) VALUES (%s)", (book["id"],))
    cache.delete(RANKING_CACHE_KEY)


if __name__ == "__main__":
    reset_and_seed_books()
    print("テストデータを投入しました")
