from fastapi import APIRouter, HTTPException, Depends, Query, Response
from datetime import datetime
from app.models.article import Article, ArticleOut
from app.services.clickhouse_client import client
from app.core.security import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import csv
import io

router = APIRouter(prefix="/articles", tags=["Articles"])
security = HTTPBearer()

def jwt_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=403, detail="Invalid token")
    return payload

@router.get("/", response_model=list[ArticleOut])
def list_articles(skip: int = 0, limit: int = 10, q: str = ""):
    query = f"""
        SELECT * FROM articles
        WHERE title ILIKE '%{q}%'
        ORDER BY id
        LIMIT {limit} OFFSET {skip}
    """
    rows = client.query(query).result_rows
    return [ArticleOut(id=r[0], title=r[1], content=r[2], created_at=r[3]) for r in rows]

@router.get("/export")
def export_articles():
    rows = client.query("SELECT * FROM articles ORDER BY id").result_rows
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "content", "created_at"])
    writer.writerows(rows)
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=articles.csv"
    return response

@router.get("/{id}", response_model=ArticleOut)
def get_article(id: int):
    rows = client.query("SELECT * FROM articles WHERE id = %(id)s", parameters={"id": id}).result_rows
    if not rows:
        raise HTTPException(status_code=404, detail="Article not found")
    r = rows[0]
    return ArticleOut(id=r[0], title=r[1], content=r[2], created_at=r[3])

@router.post("/", response_model=ArticleOut, dependencies=[Depends(jwt_auth)])
def create_article(article: Article):
    max_id = client.query("SELECT max(id) FROM articles").result_rows[0][0] or 0
    new_id = max_id + 1
    now = datetime.now()
    client.insert("articles", [(new_id, article.title, article.content, now)],
                 column_names=["id", "title", "content", "created_at"])
    return ArticleOut(id=new_id, title=article.title, content=article.content, created_at=now)

@router.put("/{id}", response_model=ArticleOut, dependencies=[Depends(jwt_auth)])
def update_article(id: int, article: Article):
    exists = client.query("SELECT * FROM articles WHERE id = %(id)s", parameters={"id": id}).result_rows
    if not exists:
        raise HTTPException(status_code=404, detail="Article not found")
    now = datetime.now()
    client.command("ALTER TABLE articles DELETE WHERE id = %(id)s", parameters={"id": id})
    client.insert("articles", [(id, article.title, article.content, now)],
                 column_names=["id", "title", "content", "created_at"])
    return ArticleOut(id=id, title=article.title, content=article.content, created_at=now)

@router.delete("/{id}", dependencies=[Depends(jwt_auth)])
def delete_article(id: int):
    client.command("ALTER TABLE articles DELETE WHERE id = %(id)s", parameters={"id": id})
    return {"message": f"Article {id} deleted"}