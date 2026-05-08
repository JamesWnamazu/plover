"""
Creates central database, calls database models

Houses three components:
engine:         - SQL Model engine, connects to SQLite
get_session:    - returns a new database session
init_db:        - creates all tables

"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """
    Yield a new database session and close it when done.
    Use as a FastAPI dependency: session: Session = Depends(get_session)
    """
    with Session(engine) as session:
        yield session


def init_db():
    """
    Create all tables defined by SQLModel subclasses.

    Models must be imported before calling create_all so that
    SQLModel registers their table definitions in metadata.
    Safe to call multiple times; existing tables are not recreated.
    """
    # These imports look unused, but they're required.
    # SQLModel only knows about a table if the model class has been
    # imported into Python's memory. Without these, create_all
    # silently creates zero tables. Don't remove them.
    import models.board    # registers "board" table
    import models.post     # registers "post" table

    SQLModel.metadata.create_all(engine)