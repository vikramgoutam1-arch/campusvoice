from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ==========================================
# 👤 USER SCHEMAS (Corey Baseline + Campus Upgrades)
# ==========================================

# Base properties shared when creating or reading a user
class UserBase(BaseModel):
    username: str
    email: EmailStr
    college_name: str
    department: str
    semester: int = Field(..., ge=1, le=8, description="Semester must be between 1 and 8")

# What the API expects during Registration (Sign-up)
class UserCreate(UserBase):
    password: str

# What the API returns when viewing a User profile (Hides the password!)
class UserResponse(BaseModel):
    id: int
    username: str
    college_name: str
    department: str
    semester: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# 💬 COMMENT SCHEMAS (Threaded Tree Layout)
# ==========================================

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None  # If populated, this comment is a nested reply!

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    author_id: int
    parent_id: Optional[int]
    created_at: datetime
    author: UserResponse  # Nesting user details into the comment view

    class Config:
        from_attributes = True


# ==========================================
# 📝 POST SCHEMAS (Categorized Extensions)
# ==========================================

class PostCreate(BaseModel):
    title: str
    content: str
    category: str
    tags: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: Optional[str] = None
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):
    content: str
    post_id: int
    parent_id: Optional[int] = None

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    parent_id: Optional[int] = None
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True