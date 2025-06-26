from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from faker import Faker
import clickhouse_connect

app = FastAPI(title="Artikel API dengan ClickHouse")

# Koneksi ClickHouse
client = clickhouse_connect.get_client(host='localhost', port=8123)

# Buat tabel kalau belum ada
def create_table():
    client.command("""
        CREATE TABLE IF NOT EXISTS articles (
            id UInt32,
            title String,
            content String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY id
    """)

create_table()

# Inisialisasi Faker untuk data palsu
faker = Faker('id_ID')

# Generate 100 data dummy
data = []
for i in range(1, 101):
    title = faker.sentence(nb_words=6)
    content = faker.paragraph(nb_sentences=5)
    created_at = datetime.now()
    data.append((i, title, content, created_at))

# ✅ Insert ke ClickHouse dengan method .insert()
client.insert(
    table='articles',
    data=data,
    column_names=['id', 'title', 'content', 'created_at']
)

print("✅ 100 artikel dummy berhasil dimasukkan.")

# ----------------- Pydantic Schemas -------------------

class Article(BaseModel):
    title: str
    content: str

class ArticleOut(Article):
    id: int
    created_at: datetime

# -------------------- CRUD API ------------------------

@app.get("/articles", response_model=list[ArticleOut])
def get_articles():
    rows = client.query("SELECT * FROM articles ORDER BY id").result_rows
    return [ArticleOut(id=r[0], title=r[1], content=r[2], created_at=r[3]) for r in rows]

@app.get("/articles/{id}", response_model=ArticleOut)
def get_article(id: int):
    rows = client.query(
        "SELECT * FROM articles WHERE id = %(id)s",
        parameters={"id": id}
    ).result_rows
    if not rows:
        raise HTTPException(status_code=404, detail="Article not found")
    r = rows[0]
    return ArticleOut(id=r[0], title=r[1], content=r[2], created_at=r[3])

@app.post("/articles", response_model=ArticleOut)
def create_article(article: Article):
    rows = client.query("SELECT max(id) FROM articles").result_rows
    next_id = (rows[0][0] or 0) + 1
    now = datetime.now()
    client.insert(
        table='articles',
        data=[(next_id, article.title, article.content, now)],
        column_names=['id', 'title', 'content', 'created_at']
    )
    return ArticleOut(id=next_id, title=article.title, content=article.content, created_at=now)

@app.put("/articles/{id}", response_model=ArticleOut)
def update_article(id: int, article: Article):
    exists = client.query(
        "SELECT * FROM articles WHERE id = %(id)s",
        parameters={"id": id}
    ).result_rows
    if not exists:
        raise HTTPException(status_code=404, detail="Article not found")
    now = datetime.now()
    client.command("ALTER TABLE articles DELETE WHERE id = %(id)s", parameters={"id": id})
    client.insert(
        table='articles',
        data=[(id, article.title, article.content, now)],
        column_names=['id', 'title', 'content', 'created_at']
    )
    return ArticleOut(id=id, title=article.title, content=article.content, created_at=now)

@app.delete("/articles/{id}")
def delete_article(id: int):
    client.command("ALTER TABLE articles DELETE WHERE id = %(id)s", parameters={"id": id})
    return {"message": f"Article {id} deleted"}
