# 🎓 CampusVoice

A verified student community platform where college students share projects, internship experiences, GATE advice, and campus life.

🔗 **Live Demo:** [campusvoice-production.up.railway.app](https://campusvoice-production.up.railway.app)

![CampusVoice Screenshot](screenshot.png)

## 🚀 Features

- JWT authentication (register/login/logout) with secure cookie-based sessions
- College email verification — only verified students can register
- Create posts with categories and tags
- Threaded comments and nested replies
- Category filter sidebar (GATE, Internship, Career, Project, Resources, Campus)
- User profiles showing post history
- Admin moderation — flagged content can be removed
- Fully containerized with Docker
- Deployed on Railway with PostgreSQL

## 🛠 Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** Jinja2 Templates, Tailwind CSS
- **Auth:** JWT tokens with bcrypt password hashing
- **Infrastructure:** Docker, Docker Compose, Railway

## ⚙️ Run Locally

1. Clone the repo
```bash
   git clone https://github.com/vikramgoutam1-arch/campusvoice.git
   cd campusvoice
```

2. Create a `.env` file in the root directory
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

## 👤 Author

Built by [Vikram Goutam](https://github.com/vikramgoutam1-arch) — final year CS engineering student.
