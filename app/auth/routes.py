from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.schemas import SignupRequest, LoginRequest, UserUpdate
from app.auth.models import User
from app.utils.security import get_current_user, hash_password, verify_password, create_access_token

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(user: SignupRequest, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        shopname=user.shopname,  # Add this field
        phone_number=user.phone_number,  # Add this field
        shop_address = user.shop_address
        )
    db.add(new_user)
    db.commit()
    return {"msg": "Signup successful"}

@auth_router.post("/login")
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}



@auth_router.put("/update-profile", response_model=UserUpdate)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Get current user from database
        user = db.query(User).filter(User.id == current_user.id).first()

        # Check if email is being updated and if it's already taken
        if user_update.email and user_update.email != user.email:
            existing_user = db.query(User).filter(User.email == user_update.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

        # Update user fields if provided
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(user, field, value)

        # Save changes to database
        db.commit()
        db.refresh(user)

        return user

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user profile: {str(e)}"
        )