from fastapi import FastAPI, Request, status
from pydantic import BaseModel
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from typing import List

app=FastAPI()
class Tache(BaseModel):
    id:int
    titre:str
    description:str

tache_global:List[Tache]=[]

@app.post("/tasks")
def ajouter_root(tache_recu:List[Tache]):
    for t in tache_recu:
        tache_global.append(t)
    return {"Message":"votre tache a été ajouter"}


@app.get("/affiche")
def afficher_root():
    return tache_global


@app.delete("/delete")
def supprimer_root(id:int):
    for t in tache_global:
        if t.id == id:
            tache_global.remove(t)
            return {"message": f"Tâche avec ID {id} supprimée."}
    return {"message": f"Aucune tâche trouvée avec l'ID {id}."}
