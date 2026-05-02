from typing import Dict

from fastapi import FastAPI

from app.api.internal import metadata as internal_metadata
from app.api.secure import auth as secure_auth
from app.api.secure import path_traversal as secure_path
from app.api.secure import sqli as secure_sqli
from app.api.secure import ssrf as secure_ssrf
from app.api.secure import users as secure_users
from app.api.vulnerable import auth as vulnerable_auth
from app.api.vulnerable import path_traversal as vulnerable_path
from app.api.vulnerable import sqli as vulnerable_sqli
from app.api.vulnerable import ssrf as vulnerable_ssrf
from app.api.vulnerable import users as vulnerable_users
from app.db.models import Base
from app.db.seed import seed_users
from app.db.session import SessionLocal, engine

app = FastAPI(title="FastAPI Security Lab")
# BOLA:
app.include_router(vulnerable_users.router)
app.include_router(secure_users.router)
# SQLi:
app.include_router(vulnerable_sqli.router)
app.include_router(secure_sqli.router)
# SSRF:
app.include_router(internal_metadata.router)
app.include_router(vulnerable_ssrf.router)
app.include_router(secure_ssrf.router)
# Path traversal
app.include_router(vulnerable_path.router)
app.include_router(secure_path.router)
# Rate limit
app.include_router(vulnerable_auth.router)
app.include_router(secure_auth.router)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initialize database schema.

    NOTE:
        This is for development only.
        In production, migrations (Alembic) should be used.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()


@app.get("/", response_model=Dict[str, str])
def root() -> Dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dict[str, str]: A simple message confirming the service is running.
    """
    return {"message": "Security Lab is running"}
