from app.db.models import Base
from app.db.seed import seed_users
from app.db.session import SessionLocal, engine


def init() -> None:
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
