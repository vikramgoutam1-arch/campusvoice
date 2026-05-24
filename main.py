from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
 
from database import engine, Base, get_db
from routers import auth, posts, users, comments
import models
 
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)
 
app = FastAPI(title="CampusVoice")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
 
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(comments.router)
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
 
def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if not user_id:
            return None
        return db.query(models.User).filter(models.User.id == user_id).first()
    except JWTError:
        return None
 
# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request, category: str = None,
         db: Session = Depends(get_db),
         current_user=Depends(get_current_user_from_cookie)):
    query = db.query(models.Post)
    if category:
        query = query.filter(models.Post.category == category)
    all_posts = query.order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse("home.html", {
        "request": request, "posts": all_posts,
        "current_user": current_user, "selected_category": category
    })
 
# NEW POST FORM — MUST be above /{post_id}
@app.get("/posts/new", response_class=HTMLResponse)
def new_post_form(request: Request, current_user=Depends(get_current_user_from_cookie)):
    if not current_user:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse("new_post.html", {
        "request": request, "current_user": current_user
    })
 
# CREATE POST
@app.post("/posts/new")
def create_post_page(request: Request,
                     title: str = Form(...), content: str = Form(...),
                     category: str = Form(...), tags: str = Form(""),
                     db: Session = Depends(get_db),
                     current_user=Depends(get_current_user_from_cookie)):
    if not current_user:
        return RedirectResponse("/login", status_code=302)
    new_post = models.Post(title=title, content=content,
                           category=category, tags=tags,
                           author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return RedirectResponse(f"/posts/{new_post.id}", status_code=302)
 
# SINGLE POST — MUST be below /new
@app.get("/posts/{post_id}", response_class=HTMLResponse)
def post_page(post_id: int, request: Request,
              db: Session = Depends(get_db),
              current_user=Depends(get_current_user_from_cookie)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    top_comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id,
        models.Comment.parent_id == None
    ).order_by(models.Comment.created_at.asc()).all()
    return templates.TemplateResponse("post.html", {
        "request": request, "post": post,
        "comments": top_comments, "current_user": current_user
    })
 
# DELETE POST
@app.post("/posts/{post_id}/delete")
def delete_post_page(post_id: int, db: Session = Depends(get_db),
                     current_user=Depends(get_current_user_from_cookie)):
    if not current_user:
        return RedirectResponse("/login", status_code=302)
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post and post.author_id == current_user.id:
        db.delete(post)
        db.commit()
    return RedirectResponse("/", status_code=302)
 
# ADD COMMENT
@app.post("/posts/{post_id}/comments")
def add_comment(post_id: int,
                content: str = Form(...), parent_id: int = Form(None),
                db: Session = Depends(get_db),
                current_user=Depends(get_current_user_from_cookie)):
    if not current_user:
        return RedirectResponse("/login", status_code=302)
    comment = models.Comment(content=content, post_id=post_id,
                             author_id=current_user.id, parent_id=parent_id)
    db.add(comment)
    db.commit()
    return RedirectResponse(f"/posts/{post_id}", status_code=302)
 
# LOGIN
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "current_user": None})
 
@app.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...),
                 db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Invalid email or password", "current_user": None
        })
    from routers.auth import create_access_token
    token = create_access_token({"user_id": user.id})
    response = RedirectResponse("/", status_code=302)
    response.set_cookie("access_token", token, httponly=True, max_age=604800)
    return response
 
# REGISTER
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "current_user": None})
 
@app.post("/register")
def register_submit(request: Request,
                    username: str = Form(...),
                    email: str = Form(...),
                    password: str = Form(...),
                    college_name: str = Form(...),
                    department: str = Form(...),
                    semester: int = Form(...),
                    db: Session = Depends(get_db)):
    
    if not email.endswith("@sirt.ac.in"):
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Only SIRT college emails (@sirt.ac.in) are allowed to register.",
            "current_user": None
        })

    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        return templates.TemplateResponse("register.html", {
            "request": request, "error": "Email already registered. Please login.", "current_user": None
        })
    hashed = pwd_context.hash(password)
    user = models.User(username=username, email=email, password=hashed,
                       college_name=college_name, department=department, semester=semester)
    db.add(user)
    db.commit()
    db.refresh(user)
    from routers.auth import create_access_token
    token = create_access_token({"user_id": user.id})
    response = RedirectResponse("/", status_code=302)
    response.set_cookie("access_token", token, httponly=True, max_age=604800)
    return response
 
# LOGOUT
@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response
 
# USER PROFILE
@app.get("/users/{user_id}", response_class=HTMLResponse)
def user_profile(user_id: int, request: Request,
                 db: Session = Depends(get_db),
                 current_user=Depends(get_current_user_from_cookie)):
    profile_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not profile_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_posts = db.query(models.Post).filter(
        models.Post.author_id == user_id
    ).order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse("profile.html", {
        "request": request, "profile_user": profile_user,
        "user_posts": user_posts, "current_user": current_user
    })
@app.post("/posts/{post_id}/delete")
def delete_post_page(post_id: int,
                     db: Session = Depends(get_db),
                     current_user=Depends(get_current_user_from_cookie)):
    if not current_user:
        return RedirectResponse("/login", status_code=302)
    fresh_user = db.query(models.User).filter(
        models.User.id == current_user.id).first()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    # Author OR admin can delete
    if post and (post.author_id == current_user.id or current_user.is_admin):
        db.delete(post)
        db.commit()
        db.expire_all()
    return RedirectResponse("/", status_code=302)