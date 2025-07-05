
# FastAPI Chat Application

A real-time chat application built with FastAPI that supports JWT authentication, WebSocket messaging, PostgreSQL persistence, and role-based access control.

## 🚀 Features

- ✅ **JWT Authentication**: Secure login and signup with password hashing
- ✅ **Role-Based Access Control (RBAC)**: Restrict access to endpoints based on user roles (admin/user)
- ✅ **WebSocket Chat**: Real-time chat support via WebSockets
- ✅ **Persistent Message Storage**: Messages are stored in PostgreSQL and fetched using pagination
- ✅ **Room-based Communication**: Chatrooms with isolated conversations
  
## 🧱 Tech Stack

| Component         | Technology         |
|------------------|--------------------|
| **Backend**      | FastAPI, Python 3.10+ |
| **Database**     | PostgreSQL          |
| **ORM**          | SQLAlchemy (or SQLModel) |
| **Authentication** | JWT (via python-jose), OAuth2 |
| **WebSocket**    | FastAPI WebSocket |
| **Password Hashing** | passlib         |


## ⚙️ Setup Instructions

### ✅ Prerequisites

- Python 3.10+
- PostgreSQL 12


### 📥 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/regmiaashish/chat-app.git
cd chat-app
```

2. **Set up virtual environment:**
```bash
python -m venv venv
# Activate environment
source venv/bin/activate        # For Linux/macOS
venv\Scripts\activate         # For Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp  .env
# Edit .env
DATABASE_URL=postgresql://user:password@localhost:5432/chatdb
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🗃️ Database Setup

1. **Create PostgreSQL Database:**
```bash
psql -U postgres -c "CREATE DATABASE chatdb;"
```

2. **Run Migrations / Create Tables:**
```python
from database import Base, engine
Base.metadata.create_all(bind=engine)
```

## ▶️ Running the Application

```bash
uvicorn main:app --reload
```

Open interactive docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🔐 API Endpoints

| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| POST   | `/users/signup`         | Register new user               |
| POST   | `/users/login`          | Login and get JWT token         |
| GET    | `/rooms/{id}/messages`  | Get paginated chat history      |
| WS     | `/ws/{room_id}`         | WebSocket for real-time chat    |

## 📦 Database Models

- **User**: `id`, `username`, `hashed_password`, `role`
- **Room**: `id`, `name`, `description`
- **Message**: `id`, `content`, `timestamp`, `user_id`, `room_id`

## 🧪 Testing with Postman

1. Import the Postman Collection
2. Set Environment Variable:
   - `base_url = http://localhost:8000`


## 🧑‍💻 Author

**Aashish Regmi**  
[GitHub Profile](https://github.com/regmiaashish)

