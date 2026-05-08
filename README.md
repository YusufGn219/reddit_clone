# 🔴 Reddit Clone

A full-stack social platform built with Django, replicating 
the core features of Reddit.

## 📌 Overview

A social platform featuring community creation, post/comment system, 
voting, user following, notifications and moderator tools.
Built with a sprint-based development approach.

## ✅ Completed Features

- 👤 User system — registration, login, profile, following, email verification
- 🏘️ Communities — creation, membership, moderator management, banner upload
- 📝 Post system — create, edit, delete, search
- 🗨️ Nested comment system — recursive render
- 👍 AJAX voting — upvote/downvote without page reload
- 🔔 Notification system — comment, follow, award notifications
- 🔒 Security — django-ratelimit, password reset, user enumeration protection
- 🧪 Test coverage — unit, integration, permission tests

## 🔄 In Progress

Saved Posts, Community Rules, User Karma, Direct Messages

## 🚀 Installation

**Requirements:** Python 3.10+, pip

```bash
# 1. Clone the repository
git clone https://github.com/YusufGn219/reddit_clone.git
cd reddit_clone

# 2. Create virtual environment
python -m venv venv
Set-ExecutionPolicy Unrestricted -Scope Process
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver
```

Go to http://localhost:8000 in your browser.

## 📁 Project Structure

| Module | Description |
|--------|-------------|
| `accounts/` | Authentication, registration, login, profile, following |
| `communities/` | Community creation, moderation, membership management |
| `posts/` | Post and comment system, service logic, template tags |
| `votes/` | Upvote/downvote logic |
| `config/` | URL routing, environment-based settings |
| `templates/` | HTML templates for all apps |
| `static/` | CSS and frontend assets |

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=flat&logo=bootstrap&logoColor=white)
