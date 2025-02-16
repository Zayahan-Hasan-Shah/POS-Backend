from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String, nullable=True)
    company_name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
