# TaskFlow

TaskFlow is a minimal but real task management system backend. Users can register, log in, create projects, add tasks to those projects, and assign tasks.

## 1. Overview

This is the backend for TaskFlow, built with **Python (FastAPI)** and **PostgreSQL**. It provides a RESTful API with authentication, relational data management, and concurrency controls.

**Tech Stack:**
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Async)
- **Migrations:** Alembic
- **Logging:** Structlog (JSON format)
- **Package Manager:** uv

## 2. Architecture Decisions

- **Language Choice**: I chose Python with FastAPI instead of Go because I am more productive with it and it allows for rapid development while maintaining high performance with async support.
- **Schema Refactoring**: Refactored Pydantic schemas to use Pydantic v2 standards (`model_config`) to avoid deprecation warnings.
- **Structured Logging**: Implemented `structlog` to provide structured JSON logs, fulfilling the requirement for structured logging (slog/zap/logrus equivalents in Python).
- **Concurrency Control**: Used pessimistic locking (`with_for_update()`) in task updates and deletions to prevent race conditions (lost updates) when multiple users operate on the same task simultaneously. Also locked projects during task creation to prevent adding tasks to a deleting project.
- **Migrations**: Used Alembic as it is the standard and most robust migration tool for SQLAlchemy.

## 3. Running Locally

Assume you have Docker installed.

1.  Clone the repository (if not already done):
    ```bash
    git clone https://github.com/purvi-n/taskflow-purvi.git
    cd zmt
    ```
2.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
3.  Start the application using Docker Compose:
    ```bash
    docker compose up
    ```
    The API will be available at `http://localhost:8000`.

## 4. Running Migrations

Migrations run **automatically** on container start. The `docker-compose.yml` includes a command to run `alembic upgrade head` before starting the FastAPI server.

If you need to run them manually, you can use:
```bash
docker compose exec web /app/.venv/bin/alembic upgrade head
```

## 5. Test Credentials

The database is automatically seeded with a test user and sample data on first run if you run the seed script.

**Seed User:**
- **Email:** `test@example.com`
- **Password:** `password123`

To run the seed script manually:
```bash
docker compose exec web /app/.venv/bin/python -m app.db.seed
```

## 6. API Reference

All non-auth endpoints require `Authorization: Bearer <token>`.

### Auth
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Projects
- `GET /projects` - List projects (paginated, supports `?page=&limit=`)
- `POST /projects` - Create a project
- `GET /projects/{id}` - Get project details with tasks
- `PATCH /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project and its tasks
- `GET /projects/{id}/stats` - Get task counts by status and assignee

### Tasks
- `GET /projects/{id}/tasks` - List tasks for a project (paginated, supports `?page=&limit=`)
- `POST /projects/{id}/tasks` - Create a task
- `GET /tasks/{id}` - Get task details
- `PATCH /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

## 7. What You'd Do With More Time

- **Test Coverage**: Add more unit tests for edge cases and concurrency scenarios.
- **Frontend**: Build the React frontend as specified in the requirements.
- **Real-time Updates**: Implement WebSockets or SSE for real-time task updates.
- **Soft Deletes**: Implement soft deletes for projects and tasks instead of hard deletes.
