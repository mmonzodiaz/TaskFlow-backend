# Kanban Backend (FastAPI listo para usar)
## Requisitos
- Python 3.10+

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Configuración opcional
Crea un archivo `.env` en la raíz para sobreescribir valores por defecto:
```
SECRET_KEY=pon_una_clave_segura
DATABASE_URL=sqlite:///./kanban.db
```

Y puedes modificar en settings.py lo que consideres necesario.

En producción, establece `COOKIE_SECURE=true` y restringe CORS (`allow_origins`).

## Endpoints principales
- **Auth**: `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`
- **Users**: `/users/me`, `/users/` (demo)
- **Boards**: `POST /boards/`, `GET /boards/`, `PATCH /boards/{id}`, `DELETE /boards/{id}`
- **Groups**: `POST /groups/`, `GET /boards/{board_id}/groups`, `PATCH /groups/{id}`, `DELETE /groups/{id}`
- **Tasks**: `POST /tasks/`, `GET /boards/{board_id}/tasks`, `GET /groups/{group_id}/tasks`, `PATCH /tasks/{id}`, `POST /tasks/{id}/move`, `DELETE /tasks/{id}`

## Notas
- Base de datos por defecto: SQLite (`kanban.db`).
- Refresh token via cookie **HttpOnly**.
- Política de contraseñas mínima y bloqueo por intentos fallidos (cache en memoria).