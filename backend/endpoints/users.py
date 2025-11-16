from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

from models.user import User, UserRole

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for demo purposes
users_db = {}

# Response models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.USER

class UserResponse(User):
    class Config:
        from_attributes = True

# Routes
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    if user.email in [u.email for u in users_db.values()]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # In a real app, you would hash the password here
    db_user = User(
        email=user.email,
        password_hash=user.password,  # In real app, hash this!
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role
    )
    
    users_db[str(db_user.id)] = db_user
    return db_user

@router.get("/", response_model=List[UserResponse])
async def list_users(role: Optional[UserRole] = None):
    """List all users, optionally filtered by role"""
    if role:
        return [user for user in users_db.values() if user.role == role]
    return list(users_db.values())

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID):
    """Get a specific user by ID"""
    if str(user_id) not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[str(user_id)]

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user_update: UserCreate):
    """Update a user"""
    if str(user_id) not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # In a real app, you would hash the password if it's being updated
    updated_user = User(
        id=user_id,
        email=user_update.email,
        password_hash=user_update.password,  # In real app, hash this!
        first_name=user_update.first_name,
        last_name=user_update.last_name,
        role=user_update.role
    )
    
    users_db[str(user_id)] = updated_user
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID):
    """Delete a user"""
    if str(user_id) not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del users_db[str(user_id)]
    return None