# pizza-api

FastAPI + PostgreSQL backend for the Fast React Pizza Co. storefront. Menu, ordering, and order-lifecycle tracking, backed by real persistence instead of an in-memory or third-party store.

## API

All routes are prefixed `/api/v1`.

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/menu` | none | List pizzas |
| POST | `/order` | none | Place an order |
| GET | `/order/{id}` | none | Look up one order |
| PATCH | `/order/{id}` | none | Toggle `priority` on an order |
| GET | `/order` | admin | List orders, optional `?status=` filter |
| PATCH | `/order/{id}/status` | admin | Advance order status |
| POST | `/auth/login` | none | Get a JWT for kitchen operations |

`GET /healthz` outside the `/api/v1` prefix pings the database.

Order status moves one step at a time: `preparing` → `out-for-delivery` → `delivered`. Skipping a step returns `400`.

Pricing is computed server-side: subtotal from menu prices × quantities, plus a 20% fee if `priority` is set — never trusted from the client.

Interactive docs at `/docs` once running.

## Run it

```bash
cp .env.example .env   # then generate ADMIN_PASSWORD_HASH, see below
docker compose up --build   # from the repo root, not this directory
```

## Develop

```bash
python -m venv .venv && .venv/Scripts/activate   # or source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
python seed.py
pytest -v
ruff check app tests seed.py
```

Tests run against a real PostgreSQL database (`TEST_DATABASE_URL`, defaults to `localhost:5432/pizza_test`) — no mocking of the DB layer, each test rolls back its own transaction for isolation.

## Generate an admin password hash

```bash
python -c "from app.security import hash_password; print(hash_password('your-password'))"
```

Set the result as `ADMIN_PASSWORD_HASH` in your environment.

## Migrations

```bash
alembic revision -m "description"   # new migration
alembic upgrade head                # apply
```

## License

MIT
