# Fast React Pizza Co.

[![CI](https://github.com/OFFiciaLFreeman01/fast-react-pizza/actions/workflows/ci.yml/badge.svg)](https://github.com/OFFiciaLFreeman01/fast-react-pizza/actions/workflows/ci.yml)

A pizza ordering app: React storefront + a real backend I built for it.

## Where this came from

The `frontend/` started as the project from Jonas Schmedtmann's Ultimate React
Course — that's where I learned React, and the storefront (menu, cart,
checkout, order tracking) follows the course closely. It originally called
Jonas's own hosted API for menu and order data.

`backend/` is new: a FastAPI + PostgreSQL service I designed and built to
replace that dependency with real infrastructure — persistence, migrations,
validation, auth, and tests — plus a `/kitchen` admin dashboard on the
frontend that the course project doesn't have. That's the part meant to
demonstrate backend engineering rather than following a tutorial.

## Architecture

```
frontend/   React storefront (Vite, Redux Toolkit, React Router, Tailwind)
backend/    pizza-api: FastAPI + PostgreSQL, Alembic migrations, pytest suite
```

The frontend talks to the backend over REST (`VITE_API_URL`, defaults to
`http://localhost:8000`). See [backend/README.md](backend/README.md) for the
API surface and [frontend/README.md](frontend/README.md) for the storefront.

## What the backend adds over the original API

- **Real persistence**: PostgreSQL with SQLAlchemy models and Alembic
  migrations, not an in-memory or third-party store.
- **Order lifecycle**: orders move `preparing` → `out-for-delivery` →
  `delivered`, with invalid transitions rejected server-side. The original
  course API had no status tracking at all.
- **JWT-protected kitchen operations**: listing all orders and advancing
  order status require a bearer token issued via `/api/v1/auth/login`.
  Everything customer-facing (menu, placing an order, checking one order's
  status) stays public, matching the original app's behavior.
- **Server-side validation**: cart items are checked against real menu rows
  (unknown pizza IDs and sold-out items are rejected), phone numbers and
  cart contents are validated, and pricing (including the 20% priority-order
  fee) is computed server-side rather than trusted from the client.
- **A `/kitchen` dashboard**: a small admin UI on top of the new endpoints —
  sign in, see live orders, filter by status, advance them one step at a
  time.

## Run it locally

```bash
docker compose up --build
```

This starts Postgres and the API (migrations + menu seed run automatically
on container start) on `http://localhost:8000`. Then, in a separate
terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The default dev admin login for `/kitchen` is `admin` / `admin123` — see
[docker-compose.yml](docker-compose.yml), and change it before deploying
anywhere real (set `ADMIN_PASSWORD_HASH` to a hash of your own password, see
[backend/.env.example](backend/.env.example)).

## Tests & CI

Backend tests run against a real Postgres instance (not mocked) — locally
via a throwaway container, in CI via a GitHub Actions Postgres service. See
[.github/workflows/ci.yml](.github/workflows/ci.yml): backend lint + test +
Docker build, frontend lint + build.
