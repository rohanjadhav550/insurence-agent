# Database & Migrations

This app talks to two separate MySQL databases:

| Env var        | Database         | Owned by             | Tables used                                          |
|-----------------|------------------|----------------------|-------------------------------------------------------|
| `DB_URL`        | `insurence_agent`| This app             | `threads`, `conversations`, `messages`                |
| `B2B_DB_URL`    | `yii2advanced`   | External B2B system  | `partner`, `loan_request`, `city` (read-only, via tools) |

Alembic migrations in this repo manage **only** the `insurence_agent` database
(`DB_URL`). The B2B database's schema belongs to that external system and is
never migrated from here — it's queried read-only via the tools in
`app/tools/`.

## Tables (insurence_agent)

- **threads** — one row per chat session (`thread_id`), created on `/api/thread/new` and `/api/conversation/new`.
- **conversations** — one row per thread, holding the sidebar `title` and `updated_at` used for ordering in `/api/conversations`.
- **messages** — chat history rows (`role`, `content`) scoped to a `thread_id`, used to render and replay a conversation.

`conversations.thread_id` and `messages.thread_id` both have a foreign key to
`threads.thread_id` with `ON DELETE CASCADE`, so deleting a thread cleans up
its conversation and messages.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requierment.txt
```

Make sure `.env` has `DB_URL` pointing at the `insurence_agent` database, e.g.:

```
DB_URL="mysql+pymysql://<user>:<password>@<host>:<port>/insurence_agent"
```

The target database (e.g. `insurence_agent`) must already exist — Alembic
creates tables inside it, not the database itself:

```sql
CREATE DATABASE insurence_agent;
```

## Running migrations

Apply all pending migrations:

```bash
alembic upgrade head
```

Check the current revision applied to the database:

```bash
alembic current
```

Roll back the most recent migration:

```bash
alembic downgrade -1
```

Roll back everything (drops all managed tables):

```bash
alembic downgrade base
```

## Creating a new migration

```bash
alembic revision -m "describe the change"
```

This scaffolds a new file under `migrations/versions/` with empty
`upgrade()`/`downgrade()` functions. This project writes migrations as plain
SQL via `op.execute(...)` (there are no SQLAlchemy ORM models to autogenerate
from — the app itself uses raw SQL too), so fill in both functions with the
`CREATE`/`ALTER`/`DROP` statements needed, keeping `downgrade()` as the exact
inverse of `upgrade()`.

Then apply it the same way:

```bash
alembic upgrade head
```
