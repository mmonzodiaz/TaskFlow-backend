from sqlalchemy.orm import Session
import models, schemas

# -------------------------
# Boards
# -------------------------
def create_board(db: Session, board: schemas.BoardCreate):
    b = models.Board(name=board.name)
    db.add(b); db.commit(); db.refresh(b)
    return b

def list_boards(db: Session):
    return db.query(models.Board).order_by(models.Board.id.asc()).all()

def update_board(db: Session, board_id: int, payload: schemas.BoardUpdate):
    b = db.get(models.Board, board_id)
    if not b: return None
    if payload.name is not None: b.name = payload.name
    db.commit(); db.refresh(b); return b

def delete_board(db: Session, board_id: int) -> bool:
    b = db.get(models.Board, board_id)
    if not b: return False
    db.delete(b); db.commit(); return True

# -------------------------
# Groups
# -------------------------
def create_group(db: Session, group: schemas.GroupCreate):
    g = models.Group(name=group.name, board_id=group.board_id, position=group.position or 0)
    db.add(g); db.commit(); db.refresh(g); return g

def list_groups_by_board(db: Session, board_id: int):
    return db.query(models.Group).filter(models.Group.board_id == board_id).order_by(models.Group.position.asc()).all()

def update_group(db: Session, group_id: int, payload: schemas.GroupUpdate):
    g = db.get(models.Group, group_id)
    if not g: return None
    if payload.name is not None: g.name = payload.name
    if payload.position is not None: g.position = payload.position
    db.commit(); db.refresh(g); return g

def delete_group(db: Session, group_id: int) -> bool:
    g = db.get(models.Group, group_id)
    if not g: return False
    db.delete(g); db.commit(); return True

# -------------------------
# Tasks
# -------------------------
def create_task(db: Session, task: schemas.TaskCreate):
    t = models.Task(
        title=task.title,
        description=task.description,
        board_id=task.board_id,
        group_id=task.group_id,
        status_id=task.status_id,
        position=task.position or 0,
    )
    db.add(t); db.commit(); db.refresh(t); return t

def list_tasks_by_board(db: Session, board_id: int):
    return (
        db.query(models.Task)
        .filter(models.Task.board_id == board_id)
        .order_by(models.Task.group_id.asc().nullsfirst(), models.Task.position.asc(), models.Task.id.asc())
        .all()
    )

def list_tasks_by_group(db: Session, group_id: int):
    return (
        db.query(models.Task)
        .filter(models.Task.group_id == group_id)
        .order_by(models.Task.position.asc(), models.Task.id.asc())
        .all()
    )

def update_task(db: Session, task_id: int, payload: schemas.TaskUpdate):
    t = db.get(models.Task, task_id)
    if not t: return None
    for field in ("title","description","status_id","group_id","board_id","position"):
        val = getattr(payload, field, None)
        if val is not None: setattr(t, field, val)
    db.commit(); db.refresh(t); return t

def move_task(db: Session, task_id: int, move: schemas.TaskMove):
    t = db.get(models.Task, task_id)
    if not t: return None
    if move.board_id is not None: t.board_id = move.board_id
    if move.group_id is not None: t.group_id = move.group_id
    if move.position is not None: t.position = move.position
    db.commit(); db.refresh(t); return t

def delete_task(db: Session, task_id: int) -> bool:
    t = db.get(models.Task, task_id)
    if not t: return False
    db.delete(t); db.commit(); return True
