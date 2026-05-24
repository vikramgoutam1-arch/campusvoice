from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, text, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True) # General login email
    password = Column(String, nullable=False)
    college_name = Column(String, nullable=False)
    department = Column(String, nullable=False)      # e.g., CSE, ECE
    semester = Column(Integer, nullable=False)       # e.g., 1, 2, 3...
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    # Relationships: If a user is deleted, cascade deletes their posts and comments
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    category = Column(String, nullable=False) 
    tags = Column(String, nullable=True) # Stored as comma-separated string for easy filtering (e.g., "GATE,OS,Python")
    # Foreign Keys
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)

    # Relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
    replies = relationship("Comment", cascade="all, delete-orphan", foreign_keys=[parent_id])

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    college_name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    # Add this new line
    is_admin = Column(Boolean, nullable=False, server_default='false')

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")