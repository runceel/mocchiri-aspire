import os

# 接続情報は Aspire の AppHost（apphost.mts）が環境変数で渡す
DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]
