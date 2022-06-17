from random import randint
from time import sleep
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='FastAPI', user='postgres', password='Tejas2911@', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as e:
        print('connection failed')
        print(e)
        sleep(5)

# my_posts = [{"title":"Armanac", "content": "The story of Armanac", "id": 1}, {"title":"Tolstoy", "content": "Tolstoy wemt to Heavenc", "id": 2}]

# def get_post_from_id(id):
#     for post in my_posts:
#         if post["id"] == id:
#             return post
#     return None


# def get_index_of_post_from_id(id):
#     for index, post in enumerate(my_posts):
#         if post["id"] == id:
#             return index
#     return None


@app.get("/")
def root():
    return {"data": "Hello World!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def put_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    return {"data": updated_post}
