from pydantic import BaseModel

class DashboardSummaryResponse(BaseModel):
    user_name : str
    shop_name: str
    shop_address : str
    total_categories: str
    total_products: str
    income_today: float
    income_month: float
    total_sales: int
    products_sold: int
    net_profit: float
    products_in_stock: int
