from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)  # e.g., "Cash" or "JazzCash"
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Link to user

    product = relationship("Product", back_populates="sales")
    user = relationship("User", back_populates="sales")  # Assuming User model has sales relationship