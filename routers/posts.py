from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.post import Post

router = APIRouter(prefix="/api/posts", tags=["posts"])

@router.get("/{board_name}")
def get_posts(board_name: str, session: Session = Depends(get_session)):
    posts = session.exec(select(Post).where(Post.board_name == board_name)).all()
    return posts

@router.post("/{board_name}")
def create_post(board_name: str, post: Post, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/{thread_id}")
def get_thread(thread_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, thread_id)
    if not post:
        raise HTTPException(status_code=404, detail="Thread not found")
    return post