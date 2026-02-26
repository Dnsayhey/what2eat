# what2eat

一个基于 FastAPI + SQLAlchemy(Async) + Alembic 的菜品管理服务。

## 环境要求

- Python `>=3.14`
- `uv` 包管理器

## 快速开始

1. 安装依赖

```bash
uv sync
```

2. 准备环境变量

```bash
cp .env.example .env
```

3. 执行数据库迁移

默认会读取 `.env` 中的配置。

```bash
uv run alembic upgrade head
```

4. 启动服务

```bash
uv run uvicorn src.main:app --reload
```

服务默认地址：`http://127.0.0.1:8000`  
文档地址：`http://127.0.0.1:8000/docs`

## 数据库配置

通过 `.env` 中 `DB_TYPE` 选择数据库：

- `DB_TYPE=sqlite`
  - 使用 `SQLITE_DB_PATH`（默认 `./data/what2eat.sqlite3`）
- `DB_TYPE=postgres`
  - 使用 `DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME`

## Alembic 迁移

生成新迁移：

```bash
uv run alembic revision -m "your migration message"
```

升级到最新版本：

```bash
uv run alembic upgrade head
```

回滚一步：

```bash
uv run alembic downgrade -1
```

## 常用接口

- `GET /health`：健康检查
- `POST /dishes`：创建菜品
- `GET /dishes`：查询菜品列表（支持分页、排序、搜索）
- `GET /dishes/{dish_id}`：查询单个菜品
- `PUT /dishes/{dish_id}`：更新菜品
- `DELETE /dishes/{dish_id}`：删除菜品
