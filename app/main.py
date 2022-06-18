from importlib.resources import contents
from multiprocessing.sharedctypes import synchronized
from time import sleep
from turtle import title
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='Tejas2911@', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break
#     except Exception as e:
#         print('connection failed')
#         print(e)
#         sleep(5)

@app.get("/")
def root():
    return {"data": "Hello World!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# def add_post(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def put_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}
