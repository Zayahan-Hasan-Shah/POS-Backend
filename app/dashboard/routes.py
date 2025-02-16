# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from datetime import datetime, timedelta
# from app.auth.models import User
# from app.database import get_db
# from app.products.models import Category, Product
# from app.sales.models import Sale
# from app.utils.security import get_current_user

# dashboard_router = APIRouter()

# # @dashboard_router.get("/summary")
# # def get_dashboard_summary(
# #     db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
# # ):
    
# #      # Get user details
# #     user_details = db.query(User).filter(User.id == current_user.id).first()
    
# #     # Get total categories for this user
# #     total_categories = db.query(Category).filter(
# #         Category.user_id == current_user.id
# #     ).count()
    
# #     # Get total products for this user
# #     total_products = db.query(Product).filter(
# #         Product.user_id == current_user.id
# #     ).count()
    
# #     # Total income today
# #     today = datetime.utcnow().date()
# #     total_income_today = (
# #         db.query(func.sum(Sale.total_price))
# #         .filter(func.date(Sale.created_at) == today)
# #         .scalar()
# #         or 0
# #     )

# #     # Total income this month
# #     current_month = datetime.utcnow().month
# #     total_income_month = (
# #         db.query(func.sum(Sale.total_price))
# #         .filter(func.extract("month", Sale.created_at) == current_month)
# #         .scalar()
# #         or 0
# #     )

# #     # Total products sold
# #     total_products_sold = db.query(func.sum(Sale.quantity)).scalar() or 0

# #     # Total sales (number of transactions)
# #     total_sales = db.query(Sale).count()

# #     # Net profit (assume profit = total income for simplicity here)
# #     net_profit = total_income_month  # Placeholder for profit calculation

# #     # Total products in stock
# #     total_products_in_stock = db.query(func.sum(Product.quantity)).scalar() or 0

# #     # Response
# #     return {
# #         "user_name": user_details.username,
# #         "shop_name": user_details.shopname,
# #         "shop_address": user_details.shop_address,
# #         "total_categories": total_categories,
# #         "total_products": total_products,
# #         "income_today": total_income_today,
# #         "income_month": total_income_month,
# #         "total_sales": total_sales,
# #         "products_sold": total_products_sold,
# #         "net_profit": net_profit,
# #         "products_in_stock": total_products_in_stock,
# #     }


# @dashboard_router.get("/summary")
# def get_dashboard_summary(
#     db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
# ):
    
#      # Get user details
#     user_details = db.query(User).filter(User.id == current_user.id).first()
    
#     # Get total categories for this user
#     total_categories = db.query(Category).filter(
#         Category.user_id == current_user.id
#     ).count()
    
#     # Get total products for this user
#     total_products = db.query(Product).filter(
#         Product.user_id == current_user.id
#     ).count()
    
#     # Total income today
#     today = datetime.utcnow().date()
#     total_income_today = (
#         db.query(func.sum(Sale.total_price))
#         .join(Product)
#         .filter(
#             func.date(Sale.created_at) == today,
#             Product.user_id == current_user.id
#         )
#         .scalar()
#         or 0
#     )

#     # Total income this month
#     current_month = datetime.utcnow().month
#     total_income_month = (
#         db.query(func.sum(Sale.total_price))
#         .join(Product)
#         .filter(
#             func.extract("month", Sale.created_at) == current_month,
#             Product.user_id == current_user.id
#         )
# .scalar()
#         or 0
#     )

#     # Total products sold
#     total_products_sold = (
#         db.query(func.sum(Sale.quantity))
#         .join(Product)
#         .filter(Product.user_id == current_user.id)
#         .scalar()
#         or 0
#     )

#     # Total sales (number of transactions)
#     total_sales = (
#         db.query(Sale)
#         .join(Product)
#         .filter(Product.user_id == current_user.id)
#         .count()
#     )

#     # Net profit (assume profit = total income for simplicity here)
#     net_profit = total_income_month  # Placeholder for profit calculation

#     # Total products in stock
#     total_products_in_stock = db.query(func.sum(Product.quantity)).scalar() or 0

#     # Response
#     return {
#         "user_name": user_details.username,
#         "shop_name": user_details.shopname,
#         "shop_address": user_details.shop_address,
#         "total_categories": total_categories,
#         "total_products": total_products,
#         "income_today": total_income_today,
#         "income_month": total_income_month,
#         "total_sales": total_sales,
#         "products_sold": total_products_sold,
#         "net_profit": net_profit,
#         "products_in_stock": total_products_in_stock,
#     }
    
# @dashboard_router.get("/chart-data")
# async def get_dashboard_charts(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     try:
#         # Get last 7 days sales trend
#         seven_days_ago = datetime.utcnow() - timedelta(days=7)
#         sales_trend = (
#             db.query(
#                 func.date(Sale.created_at).label('date'),
#                 func.sum(Sale.total_price).label('amount')
#             )
#             .join(Product)
#             .filter(
#                 Product.user_id == current_user.id,
#                 Sale.created_at >= seven_days_ago
#             )
#             .group_by(func.date(Sale.created_at))
#             .order_by(func.date(Sale.created_at))
#             .all()
#         )

#         # Get top 5 products performance
#         product_performance = (
#             db.query(
#                 Product.name,
#                 func.count(Sale.id).label('sales')
#             )
#             .join(Sale)
#             .filter(Product.user_id == current_user.id)
#             .group_by(Product.name)
#             .order_by(func.count(Sale.id).desc())
#             .limit(5)
#             .all()
#         )

#         return {
#             "salesTrend": [
#                 {
#                     "date": sale.date.strftime("%Y-%m-%d"),
#                     "amount": float(sale.amount or 0)
#                 }
#                 for sale in sales_trend
#             ],
#             "productPerformance": [
#                 {
#                     "name": product.name,
#                     "sales": int(product.sales or 0)
#                 }
#             for product in product_performance
#             ]
#         }
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error fetching dashboard data: {str(e)}"
#         )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.auth.models import User
from app.database import get_db
from app.products.models import Category, Product
from app.sales.models import Sale
from app.utils.security import get_current_user

dashboard_router = APIRouter()

@dashboard_router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        # Calculate total revenue and cost
        sales_data = (
            db.query(
                func.sum(Sale.total_price).label('total_revenue'),
                func.sum(Sale.quantity * Product.cost_price).label('total_cost')
            )
            .join(Product)
            .filter(Sale.user_id == current_user.id)
            .first()
        )

        total_revenue = float(sales_data.total_revenue or 0)
        total_cost = float(sales_data.total_cost or 0)
        net_profit = total_revenue - total_cost

        # Today's calculations
        today = datetime.now().date()
        today_sales = (
            db.query(
                func.sum(Sale.total_price).label('revenue'),
                func.sum(Sale.quantity * Product.cost_price).label('cost')
            )
            .join(Product)
 .filter(
                Sale.user_id == current_user.id,
                func.date(Sale.created_at) == today
            )
            .first()
        )

        today_revenue = float(today_sales.revenue or 0)
        today_cost = float(today_sales.cost or 0)
        today_profit = today_revenue - today_cost

        # Monthly calculations
        first_day_of_month = today.replace(day=1)
        monthly_sales = (
            db.query(
                func.sum(Sale.total_price).label('revenue'),
                func.sum(Sale.quantity * Product.cost_price).label('cost')
            )
            .join(Product)
            .filter(
                Sale.user_id == current_user.id,
                func.date(Sale.created_at) >= first_day_of_month
            )
            .first()
        )

        monthly_revenue = float(monthly_sales.revenue or 0)
        monthly_cost = float(monthly_sales.cost or 0)
        monthly_profit = monthly_revenue - monthly_cost

        # Get user details
        user_details = db.query(User).filter(User.id == current_user.id).first()
        
        # Get total categories for this user
        total_categories = db.query(Category).filter(
            Category.user_id == current_user.id
        ).count()
        
        # Get total products for this user
        total_products = db.query(Product).filter(
            Product.user_id == current_user.id
        ).count()
        
        # Total products sold
        total_products_sold = (
            db.query(func.sum(Sale.quantity))
            .join(Product)
            .filter(Product.user_id == current_user.id)
            .scalar()
or 0
        )

        # Total sales (number of transactions)
        total_sales = (
            db.query(Sale)
            .join(Product)
            .filter(Product.user_id == current_user.id)
            .count()
        )

        # Total products in stock
        total_products_in_stock = db.query(func.sum(Product.quantity)).scalar() or 0

        return {
            "user_name": user_details.username,
            "shop_name": user_details.shopname,
            "shop_address": user_details.shop_address,
            "total_categories": total_categories,
            "total_products": total_products,
            "totalRevenue": total_revenue,
            "totalCost": total_cost,
            "netProfit": net_profit,
            "todayRevenue": today_revenue,
            "todayProfit": today_profit,
            "monthlyRevenue": monthly_revenue,
            "monthlyProfit": monthly_profit,
            "total_sales": total_sales,
            "products_sold": total_products_sold,
            "products_in_stock": total_products_in_stock,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching dashboard data: {str(e)}"
        )

@dashboard_router.get("/chart-data")
async def get_dashboard_charts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Get last 7 days sales trend
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        sales_trend = (
            db.query(
                func.date(Sale.created_at).label('date'),
                func.sum(Sale.total_price).label('amount')
            )
 .join(Product)
            .filter(
                Product.user_id == current_user.id,
                Sale.created_at >= seven_days_ago
            )
            .group_by(func.date(Sale.created_at))
            .order_by(func.date(Sale.created_at))
            .all()
        )

        # Get top 5 products performance
        product_performance = (
            db.query(
                Product.name,
                func.count(Sale.id).label('sales')
            )
            .join(Sale)
            .filter(Product.user_id == current_user.id)
            .group_by(Product.name)
            .order_by(func.count(Sale.id).desc())
            .limit(5)
            .all()
        )

        return {
            "salesTrend": [
                {
                    "date": sale.date.strftime("%Y-%m-%d"),
                    "amount": float(sale.amount or 0)
                }
                for sale in sales_trend
            ],
            "productPerformance": [
                {
                    "name": product.name,
                    "sales": int(product.sales or 0)
                }
                for product in product_performance
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching dashboard data: {str(e)}"
        )