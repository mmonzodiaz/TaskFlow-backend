import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import users, boards, groups, tasks, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup...
    try:
        yield
    except asyncio.CancelledError:
        # apagado normal: evita ruido en los logs
        pass


app = FastAPI(title="Kanban Backend", version="1.0.0", lifespan=lifespan)

@app.get("/", tags=["health"])
def root():
    return {"message": "API funcionando 🚀"}

# Crea tablas al iniciar
Base.metadata.create_all(bind=engine)

# CORS (ajusta origins en producción)
app.add_middleware(
    CORSMiddleware,
    # Dominios que podrán hacer solicitudes a tu API desde el navegador.
    allow_origins=["*"],
    # Permite cookies y encabezados de autorización.
    allow_credentials=True,
    # Permite todos los métodos HTTP.
    allow_methods=["*"],
    # Permite todos los encabezados.
    allow_headers=["*"],
)

# Routers
app.include_router(users.router, tags=["users"])
app.include_router(boards.router, tags=["boards"])
app.include_router(groups.router, tags=["groups"])
app.include_router(tasks.router, tags=["tasks"])
app.include_router(auth.router, tags=["auth"])
