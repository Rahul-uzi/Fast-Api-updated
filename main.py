from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

db = {}
counter = 1

# Main model (used for create)
class Item(BaseModel):
    Name: str
    Age: float

# Update model (used for partial update)
class UpdateItem(BaseModel):
    Name: Optional[str] = None
    Age: Optional[float] = None

# Create
@app.post("/items")
def create(item: Item):
    global counter
    db[counter] = item
    item_id = counter
    counter += 1
    return {"id": item_id, **item.dict()}

# Read all
@app.get("/items")
def read_all():
    return [{"id": id, **item.dict()} for id, item in db.items()]

# Read one
@app.get("/items/{id}")
def read_one(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": id, **db[id].dict()}

# Partial Update
@app.patch("/items/{id}")
def patch_item(id: int, item: UpdateItem):
    if id not in db:
        raise HTTPException(status_code=404, detail="Item not found")

    existing_item = db[id].dict()
    update_data = item.dict(exclude_unset=True)
    existing_item.update(update_data)

    db[id] = Item(**existing_item)

    return {"id": id, **db[id].dict()}

# Delete
@app.delete("/items/{id}")
def delete(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[id]
    return {"message": "deleted"}
