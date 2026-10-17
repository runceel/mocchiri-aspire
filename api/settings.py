import os

# 接続情報は Aspire の AppHost（apphost.mts）が環境変数で渡す
DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]

# テストデータを入れ直す /admin/seed を有効にするか（AppHost が aspire run のときだけ true を渡す）
ENABLE_SEED_API = os.environ.get("ENABLE_SEED_API") == "true"
