# もっちり頒布マネージャー

技術書典のブースで使う（という設定の）頒布管理アプリです。
Azure MixBook 26H2「.NET を書かない人にこそ使ってほしい Aspire の話」のサンプルコードです。

- `before` ブランチ: Aspire 化する前の状態
- `main` ブランチ: Aspire 化した後の状態

## 構成

- `apphost.mts`: Aspire の AppHost（TypeScript）。下の 4 つをまとめて起動します
- `frontend/`: Vite + React（TypeScript）
- `api/`: Python（FastAPI）
- PostgreSQL: 本・在庫・頒布記録
- Redis: 売れ行きランキングのキャッシュ

## 必要なもの

- [Aspire CLI](https://aspire.dev/get-started/install-cli/)（13.6 以降）
- Node.js（20.19 以降、22.13 以降、または 24 以降）
- [uv](https://docs.astral.sh/uv/)（Python 3.13 以降は uv が用意します）
- Docker などのコンテナーランタイム

## 起動方法

```bash
aspire run
```

表示された URL から Aspire ダッシュボードを開き、`frontend` の URL からアプリを開きます。
PostgreSQL と Redis のデータは、AppHost を止めると消えます。

## テストデータの投入

起動するたびに、別のターミナルでテストデータを投入してください。
`DATABASE_URL` と `REDIS_URL` の値は、ダッシュボードで `api` リソースの詳細を開き、環境変数の欄で確認できます。

```bash
cd api
DATABASE_URL='<api の DATABASE_URL>' REDIS_URL='<api の REDIS_URL>' uv run python seed.py
```
