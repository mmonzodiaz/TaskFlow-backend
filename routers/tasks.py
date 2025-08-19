from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from typing import List
import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/tasks/", response_model=schemas.TaskOut, summary="Crear una tarea")
def create_task(task: schemas.TaskCreate = Body(...), db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@router.get("/boards/{board_id}/tasks", response_model=List[schemas.TaskOut], summary="Listar tareas por tablero")
def list_tasks_by_board(board_id: int = Path(...), db: Session = Depends(get_db)):
    return crud.list_tasks_by_board(db=db, board_id=board_id)

@router.get("/groups/{group_id}/tasks", response_model=List[schemas.TaskOut], summary="Listar tareas por grupo")
def list_tasks_by_group(group_id: int = Path(...), db: Session = Depends(get_db)):
    return crud.list_tasks_by_group(db=db, group_id=group_id)

@router.patch("/tasks/{task_id}", response_model=schemas.TaskOut, summary="Actualizar una tarea")
def update_task(task_id: int = Path(...), payload: schemas.TaskUpdate = Body(...), db: Session = Depends(get_db)):
    t = crud.update_task(db=db, task_id=task_id, payload=payload)
    if not t: raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return t

@router.post("/tasks/{task_id}/move", response_model=schemas.TaskOut, summary="Mover una tarea y reordenar")
def move_task(task_id: int = Path(...), move: schemas.TaskMove = Body(...), db: Session = Depends(get_db)):
    t = crud.move_task(db=db, task_id=task_id, move=move)
    if not t: raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return t

@router.delete("/tasks/{task_id}", status_code=204, summary="Eliminar una tarea")
def delete_task(task_id: int = Path(...), db: Session = Depends(get_db)):
    ok = crud.delete_task(db=db, task_id=task_id)
    if not ok: raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return None
