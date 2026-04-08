from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import json, os, time

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

DATA_FILE = "data/bookmarks.json"

def _load():
    os.makedirs("data", exist_ok=True)
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save(items):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(items, f, indent=2)

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/api/bookmarks")
async def list_items():
    return _load()

@app.post("/api/bookmarks")
async def add_item(request: Request):
    body = await request.json()
    items = _load()
    body["id"] = int(time.time() * 1000)
    body["created"] = time.strftime("%Y-%m-%d %H:%M")
    items.append(body)
    _save(items)
    return body

@app.put("/api/bookmarks/{item_id}")
async def update_item(item_id: int, request: Request):
    body = await request.json()
    items = _load()
    for i, item in enumerate(items):
        if item.get("id") == item_id:
            body["id"] = item_id
            body["created"] = item.get("created", "")
            items[i] = body
            break
    _save(items)
    return body

@app.delete("/api/bookmarks/{item_id}")
async def delete_item(item_id: int):
    items = [i for i in _load() if i.get("id") != item_id]
    _save(items)
    return {"status": "deleted"}

@app.get("/api/bookmarks/search")
async def search(q: str = ""):
    items = _load()
    if not q:
        return items
    q = q.lower()
    return [i for i in items if q in json.dumps(i).lower()]
