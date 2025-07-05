from fastapi import FastAPI
from .database import Base, engine
from .routers import users, chat

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(users.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "FastAPI Chat is running"}
