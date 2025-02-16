from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    shopname = Column(String, nullable=False)  # New field
    phone_number = Column(String, nullable=False)  # New field
    shop_address = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    sales = relationship("Sale", back_populates="user")
    categories = relationship("Category", back_populates="user") #changed