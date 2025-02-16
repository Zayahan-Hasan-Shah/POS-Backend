from fastapi import FastAPI, Depends
from app.database import Base, engine
from app.auth.routes import auth_router
from app.dashboard.routes import dashboard_router
from app.products.routes import products_router
from app.sales.routes import sales_router
from app.payments.routes import payments_router
from app.utils.security import get_current_user
from app.invoice.routes import invoice_router
from app.customer.routes import customers_router
from app.suppliers.route import supplier_router
# from app.supplier.routes import router as supplier_router

app = FastAPI(title="CRM-POS App")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])
app.include_router(payments_router, prefix="/payments", tags=["Payments"])
app.include_router(invoice_router, prefix="/invoice", tags=["Invoice"])
app.include_router(customers_router, prefix="/customers", tags=["Customers"])
app.include_router(supplier_router, prefix="/supplier", tags=["Supplier"])
# app.include_router(supplier_router, prefix="/suppliers", tags=["Suppliers"])
@app.get("/protected-route")

async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.username}!"}
