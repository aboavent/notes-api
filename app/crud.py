from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from . import models, schemas

def create_note(db: Session, data: schemas.NoteCreate) -> models.Note:
    note = models.Note(title=data.title, content=data.content or "")
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def list_notes(db: Session, limit: int = 50, offset: int = 0) -> list[models.Note]:
    stmt = select(models.Note).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())

def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    return db.get(models.Note, note_id)

def update_note(db: Session, note_id: int, data: schemas.NoteUpdate) -> Optional[models.Note]:
    note = db.get(models.Note, note_id)
    if not note:
        return None
    if data.title is not None:
        note.title = data.title
    if data.content is not None:
        note.content = data.content
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def delete_note(db: Session, note_id: int) -> bool:
    note = db.get(models.Note, note_id)
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True
