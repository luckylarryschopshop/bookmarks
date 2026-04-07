from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()
BOOKMARKS_FILE = "bookmarks.json"

if not os.path.exists(BOOKMARKS_FILE):
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump([], f)

@app.get("/")
async def read_root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/bookmarks")
async def get_bookmarks(tag: str = None):
    with open(BOOKMARKS_FILE, "r") as f:
        bookmarks = json.load(f)
    if tag:
        bookmarks = [b for b in bookmarks if tag in b.get("tags", [])]
    return bookmarks

@app.post("/api/bookmarks")
async def add_bookmark(url: str, title: str, tags: list[str]):
    with open(BOOKMARKS_FILE, "r") as f:
        bookmarks = json.load(f)
    bookmarks.append({"id": len(bookmarks), "url": url, "title": title, "tags": tags})
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bookmarks, f)
    return {"id": len(bookmarks) - 1}

@app.delete("/api/bookmarks/{id}")
async def delete_bookmark(id: int):
    with open(BOOKMARKS_FILE, "r") as f:
        bookmarks = json.load(f)
    if id >= len(bookmarks) or id < 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    del bookmarks[id]
    with open(BOOKMARKS_FILE, "w") as f:
        json.dump(bookmarks, f)
    return {"message": "Bookmark deleted"}