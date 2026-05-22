# 🎓 CampusVoice

A verified student community platform where college students share 
projects, internship experiences, GATE advice, and campus life.

## 🚀 Features
- JWT authentication (register/login/logout)
- Create posts with categories and tags
- Threaded comments and replies
- Category filter sidebar
- User profiles
- Fully containerized with Docker

## 🛠 Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** Jinja2 Templates, Tailwind CSS
- **Auth:** JWT tokens with bcrypt password hashing
- **Infrastructure:** Docker, Docker Compose

## ⚙️ Run Locally

1. Clone the repo
```bash
   git clone https://github.com/yourusername/campusvoice.git
   cd campusvoice
```

3. Run with Docker
```bash
   docker-compose up --build -d
```

4. Visit `http://localhost:8000`

## 📁 Project Structure
campusvoice/
├── routers/
│   ├── auth.py       # Register, login, JWT
│   ├── posts.py      # Post CRUD
│   ├── users.py      # User profile
│   └── comments.py   # Threaded comments
├── templates/        # Jinja2 HTML templates
├── static/           # Static files
├── main.py           # FastAPI app + page routes
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── database.py       # DB connection
├── Dockerfile
└── docker-compose.yml

2. Create `.env` file
