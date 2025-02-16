# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from app.database import Base

# class Category(Base):
#     __tablename__ = "categories"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True, nullable=False)
#     user_id = Column(Integer, nullable=False)
    
#     products = relationship("Product", back_populates="category", cascade="all, delete")

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import UniqueConstraint

class Category(Base):#changed
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="categories")
    products = relationship("Product", back_populates="category")

    _table_args_ = (
        UniqueConstraint("name", "user_id", name="unique_user_category"),
    )

# class Product(Base):
#     __tablename__ = "products"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True, nullable=False)
#     price = Column(Float, nullable=False)
#     quantity = Column(Integer, nullable=False)
#     category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
#     user_id = Column(Integer, nullable=False)
    
#     category = relationship("Category", back_populates="products")
#     sales=relationship("Sale",back_populates="product")
 
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    cost_price = Column(Float)  # Add this new field
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    
    category = relationship("Category", back_populates="products")
    sales=relationship("Sale",back_populates="product") 