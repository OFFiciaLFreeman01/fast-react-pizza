from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, menu, orders

app = FastAPI(
    title="pizza-api",
    description="Backend for the Fast React Pizza Co. storefront: menu, ordering, and a JWT-protected kitchen endpoint for tracking order status.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(auth.router)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
