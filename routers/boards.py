from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/boards/", response_model=schemas.BoardOut, summary="Crear un tablero")
def create_board(board: schemas.BoardCreate = Body(...), db: Session = Depends(get_db)):
    return crud.create_board(db=db, board=board)

@router.get("/boards/", response_model=List[schemas.BoardOut], summary="Listar tableros")
def list_boards(db: Session = Depends(get_db)):
    return crud.list_boards(db=db)

@router.patch("/boards/{board_id}", response_model=schemas.BoardOut, summary="Actualizar tablero")
def update_board(board_id: int = Path(...), payload: schemas.BoardUpdate = Body(...), db: Session = Depends(get_db)):
    b = crud.update_board(db=db, board_id=board_id, payload=payload)
    if not b: raise HTTPException(status_code=404, detail="Tablero no encontrado")
    return b

@router.delete("/boards/{board_id}", status_code=204, summary="Eliminar tablero")
def delete_board(board_id: int = Path(...), db: Session = Depends(get_db)):
    ok = crud.delete_board(db=db, board_id=board_id)
    if not ok: raise HTTPException(status_code=404, detail="Tablero no encontrado")
    return None
