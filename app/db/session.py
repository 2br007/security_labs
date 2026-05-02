import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# don't forget it is a lab :P
DATABASE_URL: str = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields:
        Session: SQLAlchemy database session.

    Ensures:
        Session is properly closed after use.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
