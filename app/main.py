from random import randint
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

my_posts = [{"title":"Armanac", "content": "The story of Armanac", "id": 1}, {"title":"Tolstoy", "content": "Tolstoy wemt to Heavenc", "id": 2}]

def get_post_from_id(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


def get_index_of_post_from_id(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None


@app.get("/")
def root():
    return {"data": "Hello World!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = get_post_from_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randint(1, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = get_index_of_post_from_id(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def put_post(id: int, post: Post):
    index = get_index_of_post_from_id(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} not found")
    
    post_dict = post.dict()
    post_dict["id"] = index
    my_posts[index] = post_dict
    return {"data": post_dict}
