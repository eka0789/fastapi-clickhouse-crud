from pydantic import BaseModel
from datetime import datetime

class Article(BaseModel):
    title: str
    content: str

class ArticleOut(Article):
    id: int
    created_at: datetime