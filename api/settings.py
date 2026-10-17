import os

from dotenv import load_dotenv

# 接続情報は .env に書いてある
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]
