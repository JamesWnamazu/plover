"""
Creates table for boards

Fields:
board_name:
board_type:
board_id:

"""

from sqlmodel import SQLModel, Field

class Board(SQLModel, table=True):
    id        : int | None = Field(default=None, primary_key=True)
    name      : str        = Field(unique=True)  # 'anime', 'tech', etc.
    category  : str                              # 'entertainment', 'study', 'hobby'