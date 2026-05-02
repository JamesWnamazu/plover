"""
Creates table for posts

Fields:
id: 
board_id:
thread_id:

title:
content:
image:
created_at:

"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Post(SQLModel, table=True):
    id         : int | None        = Field(default=None, primary_key=True)
    board_id   : int               = Field(foreign_key="board.id")
    thread_id  : int | None        = Field(default=None, foreign_key="post.id")
    
    title      : str | None        = Field(default=None)  # only thread openers have titles
    content    : str
    image      : str | None        = Field(default=None)
    created_at : datetime          = Field(default_factory=datetime.utcnow)