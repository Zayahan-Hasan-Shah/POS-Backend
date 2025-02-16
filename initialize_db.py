from app.database import engine, Base
from app.auth.models import User
from app.products.models import Category, Product
from app.sales.models import Sale

def create_tables():
    """
    Creates all database tables defined in the models.
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables()
