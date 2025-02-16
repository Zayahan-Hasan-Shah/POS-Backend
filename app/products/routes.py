from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.products.models import Category, Product
from app.products.schemas import CategoryCreate, ProductCreate, CategoryRequest, ProductResponse
from app.utils.security import get_current_user
from app.auth.models import User

products_router = APIRouter()

# ✅ CREATE CATEGORY
@products_router.post("/categories")#changed
def create_category(
    category: CategoryRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  # Ensure current_user is a User object
):
    # Check if the category already exists for the current user
    existing_category = db.query(Category).filter(
        Category.name == category.name,
        Category.user_id == current_user.id
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists for this user"
        )

    # Create and add the new category for the user
    new_category = Category(
        name=category.name,
        user_id=current_user.id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return {"message": "Category created successfully", "category":new_category}

# @products_router.post("/categories", response_model=CategoryResponse)
# def create_category(
#     category: CategoryCreate,
#     db: Session = Depends(get_db),
#     current_user: str = Depends(get_current_user),
# ):
#     category_exists = db.query(Category).filter(
#         Category.name == category.name, Category.user_id == current_user.id
#     ).first()
#     if category_exists:
#         raise HTTPException(status_code=400, detail="Category already exists")

#     new_category = Category(name=category.name, user_id=current_user.id)
#     db.add(new_category)
#     db.commit()
#     db.refresh(new_category)
#     return new_category

# ✅ GET ALL CATEGORIES
@products_router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return [{"id": category.id, "name": category.name} for category in categories]

# @products_router.get("/categories", response_model=list[CategoryRequest])
# def get_categories(
#     db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
# ):
#     return db.query(Category).filter(Category.user_id == current_user.id).all()

# ✅ UPDATE CATEGORY
@products_router.put("/categories/{category_id}", response_model=CategoryRequest)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing_category = db.query(Category).filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()

    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    existing_category.name = category.name
    db.commit()
    db.refresh(existing_category)
    return existing_category

# ✅ DELETE CATEGORY
@products_router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    category = db.query(Category).filter(
        Category.id == category_id, Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()
    return {"msg": "Category deleted successfully"}

# ✅ CREATE PRODUCT
@products_router.post("/products",status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        db_product = Product(
            name=product.name,
            price=product.price,
            cost_price=product.cost_price,
            quantity=product.quantity,
            category_id=product.category_id,
            user_id=current_user.id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error creating product: {str(e)}"
        )
# @products_router.post("/products", response_model=ProductResponse)
# def create_product(
#     product: ProductCreate,
#     db: Session = Depends(get_db),
#     current_user: str = Depends(get_current_user),
# ):
#     category = db.query(Category).filter(
#         Category.id == product.category_id, Category.user_id == current_user.id
#     ).first()

#     if not category:
#         raise HTTPException(status_code=400, detail="Category not found")

#     new_product = Product(
#         name=product.name,
#         price=product.price,
#         cost_price=product.cost_price,
#         quantity=product.quantity,
#         category_id=product.category_id,
#         user_id=current_user.id,
#     )
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product
# @products_router.post("/products", response_model=ProductResponse)
# def create_product(
#     product: ProductCreate,
#     db: Session = Depends(get_db),
#     current_user: str = Depends(get_current_user),
# ):
#     category = db.query(Category).filter(
#         Category.id == product.category_id, Category.user_id == current_user.id
#     ).first()

#     if not category:
#         raise HTTPException(status_code=400, detail="Category not found")

#     new_product = Product(
#         name=product.name,
#         price=product.price,
#         quantity=product.quantity,
#         category_id=product.category_id,
#         user_id=current_user.id,
#     )
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product

# ✅ GET ALL PRODUCTS
@products_router.get("/products", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    return db.query(Product).filter(Product.user_id == current_user.id).all()

# ✅ UPDATE PRODUCT
@products_router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    existing_product = db.query(Product).filter(
        Product.id == product_id, Product.user_id == current_user.id
    ).first()

    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.quantity = product.quantity
    existing_product.category_id = product.category_id

    db.commit()
    db.refresh(existing_product)
    return existing_product

# ✅ DELETE PRODUCT
@products_router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    product = db.query(Product).filter(
        Product.id == product_id, Product.user_id == current_user.id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"msg": "Product deleted successfully"}


# get low products
@products_router.get("/low-stock")
async def get_low_stock_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Query products with quantity less than 15
        low_stock_products = (
            db.query(Product)
            .filter(
                Product.user_id == current_user.id,
                Product.quantity < 15
            )
            .order_by(Product.quantity.asc())  # Order by quantity ascending
            .all()
        )

        # Format the response
        return [
            {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "quantity": product.quantity,
                "categoryName": product.category.name if product.category else None,
                # "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for product in low_stock_products
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching low stock products: {str(e)}"
    )