from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.sales.models import Sale
from app.products.models import Product
from app.sales.schemas import SaleRequest
from app.utils.security import get_current_user
from app.sales.models import Sale  # Or the correct path
from app.auth.models import User  # Keep this if User is in app.auth.models

sales_router = APIRouter()

# @sales_router.post("/sales")
# def add_sale(
#     sale: SaleRequest,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     product = db.query(Product).filter(Product.id == sale.product_id).first()
#     if not product:
#         raise HTTPException(status_code=400, detail="Product not found")
#     if product.quantity < sale.quantity:
#         raise HTTPException(status_code=400, detail="Insufficient stock")
    
#     total_price = product.price * sale.quantity
#     new_sale = Sale(
#         product_id=sale.product_id,
#         quantity=sale.quantity,
#         total_price=total_price,
#         payment_method=sale.payment_method,
#         user_id=current_user.id,  # Associate the sale with the current user
#     )
#     product.quantity -= sale.quantity
#     db.add(new_sale)
#     db.commit()
#     return {"msg": "Sale recorded successfully", "total_price": total_price}

# @sales_router.get("/sales")
# def get_sales_history(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Fetch sales made by the current user
#     return db.query(Sale).filter(Sale.user_id == current_user.id).all()


@sales_router.post("/sales")
def add_sale(
    sale: SaleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    if product.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    total_price = product.price * sale.quantity
    new_sale = Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        total_price=total_price,
        payment_method=sale.payment_method,
        user_id=current_user.id,  # Associate the sale with the current user
    )
    product.quantity -= sale.quantity
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    
    # Return more detailed response
    return {
        "msg": "Sale recorded successfully",
        "sale_details": {
            "id": new_sale.id,
            "product_name": product.name,
            "quantity": sale.quantity,
            "unit_price": product.price,
            "total_price": total_price,
            "payment_method": sale.payment_method,
            "date": new_sale.created_at
        }
    }

@sales_router.get("/sales")
def get_sales_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Fetch sales with product details
    sales = (
        db.query(Sale)
        .join(Product)
        .filter(Sale.user_id == current_user.id)
        .all()
    )
    
    # Return detailed sales information
    return [
        {
            "id": sale.id,
            "product_name": sale.product.name,
            "quantity": sale.quantity,
            "unit_price": sale.product.price,
            "total_price": sale.total_price,
            "payment_method": sale.payment_method,
            "date": sale.created_at
        }
        for sale in sales
        ]
    

@sales_router.get("/daily-summary")
def get_daily_sales_summary(
    date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If no date provided, use today's date
    target_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now().date()
    
    # Query for daily sales
    daily_sales = (
        db.query(
            Product.name,
            func.sum(Sale.quantity).label("total_quantity"),
            func.sum(Sale.total_price).label("total_revenue")
        )
        .join(Sale)
        .filter(
            func.date(Sale.created_at) == target_date,
            Sale.user_id == current_user.id
        )
        .group_by(Product.name)
        .all()
    )
    
    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "sales_summary": [
            {
                "product_name": name,
                "total_quantity": int(quantity),
                "total_revenue": float(revenue)
            }
            for name, quantity, revenue in daily_sales
        ]
    }

@sales_router.get("/monthly-summary")
def get_monthly_sales_summary(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If no year/month provided, use current year and month
    today = datetime.now()
    target_year = year if year else today.year
    target_month = month if month else today.month
    
    # Query for monthly sales
    monthly_sales = (
        db.query(
            Product.name,
            func.sum(Sale.quantity).label("total_quantity"),
            func.sum(Sale.total_price).label("total_revenue"),
            func.date(Sale.created_at).label("sale_date")
        )
        .join(Sale)
        .filter(
            func.extract('year', Sale.created_at) == target_year,
            func.extract('month', Sale.created_at) == target_month,
            Sale.user_id == current_user.id
        )
        .group_by(Product.name, func.date(Sale.created_at))
        .order_by(func.date(Sale.created_at))
        .all()
    )
    
    return {
        "year": target_year,
        "month": target_month,
        "sales_summary": [
            {
                "product_name": name,
                "total_quantity": int(quantity),
                "total_revenue": float(revenue),
                "date": date.strftime("%Y-%m-%d")
            }
            for name, quantity, revenue, date in monthly_sales
        ]
    }
