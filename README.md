# もっちり頒布マネージャー

技術書典のブースで使う（という設定の）頒布管理アプリです。
Azure MixBook 26H2「.NET を書かない人にこそ使ってほしい Aspire の話」のサンプルコードです。

- `before` ブランチ: Aspire 化する前の状態
- `main` ブランチ: Aspire 化した後の状態

## 構成

- `frontend/`: Vite + React（TypeScript）
- `api/`: Python（FastAPI）
- PostgreSQL: 本・在庫・頒布記録
- Redis: 売れ行きランキングのキャッシュ

## 必要なもの

- Node.js（20.19 以降、または 22.12 以降）
- [uv](https://docs.astral.sh/uv/)（Python 3.13 以降は uv が用意します）
- Docker（Docker Compose）
- bash（Windows の場合は Git Bash など）

## 起動方法

```bash
./scripts/dev.sh
```

初回は、起動したあとに別のターミナルでテストデータを投入してください。

```bash
cd api
uv run python seed.py
```

ブラウザーで http://localhost:5173 を開きます。
