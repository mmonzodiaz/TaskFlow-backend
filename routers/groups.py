from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/groups/", response_model=schemas.GroupOut, summary="Crear un grupo dentro de un tablero")
def create_group(group: schemas.GroupCreate = Body(...), db: Session = Depends(get_db)):
    return crud.create_group(db=db, group=group)

@router.get("/boards/{board_id}/groups", response_model=List[schemas.GroupOut], summary="Listar grupos de un tablero")
def list_groups(board_id: int = Path(...), db: Session = Depends(get_db)):
    return crud.list_groups_by_board(db=db, board_id=board_id)

@router.patch("/groups/{group_id}", response_model=schemas.GroupOut, summary="Actualizar un grupo")
def update_group(group_id: int = Path(...), payload: schemas.GroupUpdate = Body(...), db: Session = Depends(get_db)):
    g = crud.update_group(db=db, group_id=group_id, payload=payload)
    if not g: raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return g

@router.delete("/groups/{group_id}", status_code=204, summary="Eliminar un grupo")
def delete_group(group_id: int = Path(...), db: Session = Depends(get_db)):
    ok = crud.delete_group(db=db, group_id=group_id)
    if not ok: raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return None
