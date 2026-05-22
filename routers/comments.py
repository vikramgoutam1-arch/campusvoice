from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from routers.auth import get_current_user

router = APIRouter(prefix="/api/comments", tags=["Comments"])

# Create a comment or reply
@router.post("/", response_model=schemas.CommentResponse,
             status_code=status.HTTP_201_CREATED)
def create_comment(comment: schemas.CommentCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    
    # Check post exists
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # If it's a reply, check parent comment exists
    if comment.parent_id:
        parent = db.query(models.Comment).filter(
            models.Comment.id == comment.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent comment not found")
    
    new_comment = models.Comment(
        author_id=current_user.id,
        **comment.dict()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Get all comments for a post
@router.get("/post/{post_id}", response_model=List[schemas.CommentResponse])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id,
        models.Comment.parent_id == None  # top level only
    ).all()
    return comments

# Delete a comment
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your comment")
    db.delete(comment)
    db.commit()