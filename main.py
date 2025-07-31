from xmlrpc.client import DateTime
from fastapi import FastAPI, Request, status
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from typing import List

templates=Jinja2Templates(directory="HTML")

app=FastAPI()
@app.get("/ping")
def ping_root():
    return {"message":"pang"}

@app.get("/html", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse("file.html")


class objet(BaseModel):
    author:str
    title:str
    content:str
    creation_dateTime:DateTime

list_global:List[objet]=[]

@app.post("/posts")
def post_root(object_add:List[objet]):
    list_global.extend(object_add)
    return list_global

@app.get("/posts")
def get_root():
    return list_global

@app.put("/posts")
def put_root(title:str):
    for index in list_global:
        if index.title==title:
            list_global.append(index)
        list_global.extend(title)
        return {"message":"la mise a jour de la liste à été faite"}