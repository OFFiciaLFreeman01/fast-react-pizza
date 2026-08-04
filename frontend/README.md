# frontend

React + Vite storefront for Fast React Pizza Co. Redux Toolkit for cart/user state, React Router (data routers) for navigation, Tailwind for styling.

See the [repo root README](../README.md) for the full picture, including the backend this talks to.

## Develop

```bash
npm install
cp .env.example .env   # point VITE_API_URL at your backend
npm run dev
```

## Kitchen dashboard

`/kitchen` is a small admin view (login + order list + status updates) added on top of the original storefront, backed by the new `pizza-api` service's JWT-protected endpoints.
