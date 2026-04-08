# Bookmarks

Bookmark manager with tags

## Run

```bash
docker compose up -d
# Open http://127.0.0.1:PORT
```

## API

  - GET /api/bookmarks — list all items
  - POST /api/bookmarks — add item (send JSON body)
  - PUT /api/bookmarks/{id} — update item (send JSON body)
  - DELETE /api/bookmarks/{id} — delete item
  - GET /api/bookmarks/search?q=term — search items
