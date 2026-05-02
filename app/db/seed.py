from sqlalchemy.orm import Session

from app.db.models import User


def seed_users(db: Session) -> None:
    """
    Seed initial users into the database.

    Creates two users for BOLA testing.

    Args:
        db (Session): Database session.
    """

    if db.query(User).count() > 0:
        return

    user1 = User(username="alice", email="alice@test.com")
    user2 = User(username="bob", email="bob@test.com")

    db.add_all([user1, user2])
    db.commit()
