import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import get_db, init_db
from . import schemas, crud

app = FastAPI(title="Notes API", version="0.1.0")

# Open CORS by default (tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/notes", response_model=schemas.NoteOut, status_code=201)
def create_note(payload: schemas.NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, payload)

@app.get("/notes", response_model=list[schemas.NoteOut])
def list_notes(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    return crud.list_notes(db, limit=limit, offset=offset)

@app.get("/notes/{note_id}", response_model=schemas.NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=schemas.NoteOut)
def update_note(note_id: int, payload: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = crud.update_note(db, note_id, payload)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Note not found")
    return None
