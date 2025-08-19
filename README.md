# Kanban Backend (FastAPI ready to use)

## Requirements

-   Python 3.10+

## Installation

``` bash
python -m venv venv
venv\Scripts\activate  # on Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Optional configuration

Create a `.env` file in the project root to override default values:

    SECRET_KEY=put_a_secure_key
    DATABASE_URL=sqlite:///./kanban.db

You can also modify anything you consider necessary in `settings.py`.

In production, set `COOKIE_SECURE=true` and restrict CORS
(`allow_origins`).

## Main Endpoints

-   **Auth**: `/auth/register`, `/auth/login`, `/auth/refresh`,
    `/auth/logout`
-   **Users**: `/users/me`, `/users/` (demo)
-   **Boards**: `POST /boards/`, `GET /boards/`, `PATCH /boards/{id}`,
    `DELETE /boards/{id}`
-   **Groups**: `POST /groups/`, `GET /boards/{board_id}/groups`,
    `PATCH /groups/{id}`, `DELETE /groups/{id}`
-   **Tasks**: `POST /tasks/`, `GET /boards/{board_id}/tasks`,
    `GET /groups/{group_id}/tasks`, `PATCH /tasks/{id}`,
    `POST /tasks/{id}/move`, `DELETE /tasks/{id}`

## Notes

-   Default database: SQLite (`kanban.db`).
-   Refresh token via **HttpOnly** cookie.
-   Minimum password policy and lockout after failed attempts (in-memory
    cache).
