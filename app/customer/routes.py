from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_user
from app.customer.models import Customer
from app.customer.schemas import CustomerCreate,CustomerResponse,CustomerUpdate
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

customers_router = APIRouter()

# Create a new customer
@customers_router.post("/create-customer", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing_customer = db.query(Customer).filter(
        (Customer.email == customer.email) | (Customer.phone == customer.phone)
    ).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer with this email or phone already exists")

    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    logger.info(f"Customer created: {new_customer.name} ({new_customer.email})")
    return new_customer

# Get a single customer by ID
@customers_router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer

# Get all customers
@customers_router.get("/", response_model=list[CustomerResponse])
def get_customers(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return db.query(Customer).all()

# Update a customer's details
@customers_router.put("/single-customer/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Update only provided fields
    if customer_data.name:
        customer.name = customer_data.name
    if customer_data.email:
        customer.email = customer_data.email
    if customer_data.phone:
        customer.phone = customer_data.phone
    if customer_data.address:
        customer.address = customer_data.address

    db.commit()
    db.refresh(customer)

    return customer

# Delete a customer
@customers_router.delete("/delete-customer/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    
    return {"msg": "Customer deleted successfully"}
