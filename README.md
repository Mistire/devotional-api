# Devotional API

**Devotional API** is a RESTful backend for delivering daily Christian devotionals linked with Bible verses.
It allows users to browse, search, submit, and bookmark devotionals, with optional integration to external Bible APIs for full scripture text retrieval.

---

## Features

### Core Functionality

* **Retrieve Today's Devotional** – Get the devotional for the current date.
* **Browse Devotionals** – Filter devotionals by topic, date, or author.
* **Search Devotionals** – Search by keywords or Bible verse references.
* **Submit Devotionals** – Registered users can submit content, which is moderated before publishing.
* **Bookmarks/Favorites** – Save devotional content or verses for later reference.

### User Management

* **Registration & Authentication** – Users can register, login, and access protected endpoints using JWT.
* **Profile Management** – Users can view their profile information.

### Optional Integration

* **Bible API Integration** – Fetch full scripture text by reference from external Bible APIs.

---

## Technology Stack

* **Backend Framework:** Django, Django REST Framework
* **Database:** PostgreSQL (SQLite for development/testing)
* **Authentication:** JWT via `djangorestframework-simplejwt`
* **API Documentation:** Swagger / OpenAPI via `drf-spectacular`
* **Testing:** Django Test Framework / Pytest
* **Deployment Options:** PythonAnywhere, Render, Heroku

---

## API Endpoints (Users App)

### Authentication

| Endpoint                   | Method | Description                                                         |
| -------------------------- | ------ | ------------------------------------------------------------------- |
| `/api/auth/register/`      | POST   | Register a new user. Returns user info.                             |
| `/api/auth/login/`         | POST   | Login with email and password. Returns JWT access & refresh tokens. |
| `/api/auth/token/refresh/` | POST   | Refresh JWT access token.                                           |
| `/api/auth/profile/`       | GET    | Retrieve authenticated user profile.                                |

*(Other app endpoints will be added as development continues.)*

---

## Setup & Installation

1. **Clone the repository:**

```bash
git clone <repository-url>
cd devotional-api
```

2. **Create virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Apply migrations:**

```bash
python manage.py migrate
```

5. **Create a superuser:**

```bash
python manage.py createsuperuser
```

6. **Run development server:**

```bash
python manage.py runserver
```

7. **Access API documentation:**

```
http://127.0.0.1:8000/swagger/
```

---
