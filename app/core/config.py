import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    clickhouse_host: str = os.getenv("CLICKHOUSE_HOST", "localhost")
    clickhouse_port: int = int(os.getenv("CLICKHOUSE_PORT", 8123))
    secret_key: str = os.getenv("SECRET_KEY", "supersecret")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = 60

settings = Settings()