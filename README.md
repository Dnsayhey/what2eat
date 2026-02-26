# what2eat monorepo

前后端分目录管理：

- `backend/`：FastAPI + SQLAlchemy + Alembic
- `frontend/`：React + TypeScript + Vite + Tailwind

## Backend

```bash
cd backend
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn src.main:app --reload
```

后端地址：`http://127.0.0.1:8000`  
文档地址：`http://127.0.0.1:8000/docs`

## Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

前端地址：`http://127.0.0.1:5173`

默认会请求 `VITE_API_BASE_URL=http://127.0.0.1:8000`。
