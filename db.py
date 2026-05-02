"""
Creates central database, calls database models

Houses three components:
engine:         - SQL Model engine, connects to SQLite
get_session:    - returns a new databse session
init_db:        - creates all tables

"""

from sqlmodel import SQLModel, create_engine, Session

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
    import models.board           # registers "board" table
    import models.post   # registers "post" table

    SQLModel.metadata.create_all(engine)