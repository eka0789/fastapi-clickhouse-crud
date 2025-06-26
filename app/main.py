from fastapi import FastAPI
from app.routers import articles, auth
from app.services.clickhouse_client import create_articles_table

app = FastAPI(title="FastAPI + ClickHouse CRUD API")

# Init table on startup
create_articles_table()

# Register routers
app.include_router(auth.router)
app.include_router(articles.router)