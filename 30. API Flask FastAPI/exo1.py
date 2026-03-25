import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class User(BaseModel):
    """User model with validation"""
    id: int = Field(..., description="Unique identifier for the user")
    name: str = Field(..., min_length=2, max_length=50, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    age: int = Field(..., ge=0, le=150, description="User's age (0-150)")
    is_active: bool = Field(default=True, description="Is user active?")

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    """Endpoint to create a new user"""
    return {"message": "User created successfully", "user": user}

if __name__ == "__main__":
    uvicorn.run("exo1:app", host="127.0.0.1", port=8000, reload=True)