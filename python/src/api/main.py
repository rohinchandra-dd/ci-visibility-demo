from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import articles, auth, comments, misc
from core.config import get_settings
from core.database import init_db

settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(articles.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(misc.router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "pulse-api"}
