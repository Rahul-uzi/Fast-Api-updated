# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simple database
db = {}
counter = 1

# Model
class Item(BaseModel):
    Name: str
    Age: float

# Create
@app.post("/items")
def create(item: Item):
    global counter
    db[counter] = item
    counter += 1
    return {"id": counter-1, **item.dict()}

# Read all
@app.get("/items")
def read_all():
    return [{"id": id, **item.dict()} for id, item in db.items()]

# Read one
@app.get("/items/{id}")
def read_one(id: int):
    return {"id": id, **db[id].dict()}

# Update
@app.put("/items/{id}")
def update(id: int, item: Item):
    db[id] = item
    return {"id": id, **item.dict()}

# Delete
@app.delete("/items/{id}")
def delete(id: int):
    del db[id]
    return {"message": "deleted"}