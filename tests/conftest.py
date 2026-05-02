from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.db.seed import seed_users
from app.db.session import engine

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_test_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields:
        Session: SQLAlchemy database session.

    Ensures:
        Session is properly closed after use.
    """
    db: Session = TestingSessionLocal()
    seed_users(db)
    try:
        yield db
    finally:
        db.close()
