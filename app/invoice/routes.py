# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app.invoice.models import Invoice, InvoiceItem
# from app.invoice.schemas import InvoiceRequest
# from app.utils.security import get_current_user

# invoice_router = APIRouter()

# @invoice_router.post("/create-invoice")
# def create_invoice(invoice: InvoiceRequest, db: Session = Depends(get_db)):
#     # Calculate total amount
#     total_amount = sum(item.quantity * item.unit_price for item in invoice.items)

#     # Create invoice
#     new_invoice = Invoice(
#         customer_name=invoice.customer_name if invoice.customer_name else "Anonymous",
#         customer_phone=invoice.customer_phone if invoice.customer_phone else "1234567890",
#         total_amount=total_amount
#     )
#     db.add(new_invoice)
#     db.commit()
#     db.refresh(new_invoice)

#     # Add invoice items
#     for item in invoice.items:
#         new_item = InvoiceItem(
#             invoice_id=new_invoice.id,
#             product_name=item.product_name,
#             quantity=item.quantity,
#             unit_price=item.unit_price,
#             total_price=item.quantity * item.unit_price
#         )
#         db.add(new_item)

#     db.commit()
#     return {"msg": "Invoice created successfully", "invoice_id": new_invoice.id, "total_amount": total_amount}


# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from app.database import get_db
# from app.invoice.schemas import Invoice, InvoiceItem
# # from app.invoice.schemas import InvoiceRequest
# from app.invoice.schemas import InvoiceCreate
# from datetime import datetime
# from app.utils.security import get_current_user

# invoice_router = APIRouter()

# @invoice_router.post("/create-invoice")
# def create_invoice(invoice: InvoiceRequest, db: Session = Depends(get_db)):
#     # Calculate total amount
#     total_amount = sum(item.quantity * item.unit_price for item in invoice.items)

#     # Create invoice
#     new_invoice = Invoice(
#         customer_name=invoice.customer_name if invoice.customer_name else "Anonymous",
#         customer_phone=invoice.customer_phone if invoice.customer_phone else "1234567890",
#         total_amount=total_amount
#     )
#     db.add(new_invoice)
#     db.commit()
#     db.refresh(new_invoice)

#     # Add invoice items
#     for item in invoice.items:
#         new_item = InvoiceItem(
#             invoice_id=new_invoice.id,
#             product_name=item.product_name,
#             quantity=item.quantity,
#             unit_price=item.unit_price,
#             total_price=item.quantity * item.unit_price
#         )
#         db.add(new_item)

#     db.commit()
#     return {"msg": "Invoice created successfully", "invoice_id": new_invoice.id, "total_amount": total_amount}




# @invoice_router.post("/create", response_model=InvoiceResponse)
# async def create_invoice(
#     invoice: InvoiceCreate,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Create invoice
#         new_invoice = Invoice(
#             invoice_number=f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
#             customer_id=invoice.customer_id,
#             total_amount=invoice.total_amount,
#             payment_method=invoice.payment_method,
#             status="PAID"
#         )
#         db.add(new_invoice)
#         db.flush()  # Get the invoice ID

#         # Create invoice items
#         for item in invoice.items:
#             invoice_item = InvoiceItem(
#                 invoice_id=new_invoice.id,
#                 product_name=item.product_name,
#                 quantity=item.quantity,
#                 unit_price=item.unit_price,
#                 total_price=item.total_price
#             )
#             db.add(invoice_item)

#         db.commit()
#         db.refresh(new_invoice)
#         return new_invoice

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))



# async def create_invoice(
#     invoice: InvoiceCreate,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Create invoice
#         new_invoice = Invoice(
#             customer_name=invoice.customer_name,
#             customer_phone=invoice.customer_phone,
#             total_amount=invoice.total_amount,
#             created_at=datetime.utcnow()
#         )
#         db.add(new_invoice)
#         db.flush()  # Get the invoice ID

#         # Create invoice items
#         for item in invoice.items:
#             invoice_item = InvoiceItem(
#                 invoice_id=new_invoice.id,
#                 product_name=item.product_name,
#                 quantity=item.quantity,
#                 unit_price=item.unit_price,
#                 total_price=item.total_price
#             )
#             db.add(invoice_item)

#         db.commit()
#         db.refresh(new_invoice)
        
#         return {
#             "id": new_invoice.id,
#             "customer_name": new_invoice.customer_name,
#             "customer_phone": new_invoice.customer_phone,
#             "total_amount": new_invoice.total_amount,
#             "created_at": new_invoice.created_at,
#             "items": [
#                 {
#                     "product_name": item.product_name,
#                     "quantity": item.quantity,
#                     "unit_price": item.unit_price,
#                     "total_price": item.total_price
#                 }
#                 for item in new_invoice.items
#             ]
#         }

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# async def create_invoice(
#     invoice_data: dict,
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Create invoice
#         new_invoice = Invoice(
#             customer_name=invoice_data['customer_name'],
#             customer_phone=invoice_data['customer_phone'],
#             total_amount=invoice_data['total_amount'],
#             payment_method=invoice_data['payment_method'],
#             created_at=datetime.utcnow()
#         )
#         db.add(new_invoice)
#         db.flush()

#         # Create invoice items
#         for item_data in invoice_data['items']:
#             invoice_item = InvoiceItem(
#                 invoice_id=new_invoice.id,
#                 product_name=item_data['product_name'],
#                 quantity=item_data['quantity'],
#                 unit_price=item_data['unit_price'],
#                 total_price=item_data['total_price']
#             )
#             db.add(invoice_item)

#         db.commit()
#         db.refresh(new_invoice)

#         # Return response
#         return {
#             "id": new_invoice.id,
#             "customer_name": new_invoice.customer_name,
#             "customer_phone": new_invoice.customer_phone,
#             "total_amount": new_invoice.total_amount,
#             "payment_method": new_invoice.payment_method,
#             "created_at": new_invoice.created_at,
#             "items": [
#                 {
#                     "product_name": item.product_name,
#                     "quantity": item.quantity,
#                     "unit_price": item.unit_price,
#                     "total_price": item.total_price
#                 }
#                 for item in new_invoice.items
#             ]
#         }

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# async def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
#     try:
#         # Generate invoice number
#         invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
#         # Create invoice
#         db_invoice = Invoice(
#             customer_name=invoice.customer_name,
#             customer_phone_invoice_number=invoice.customer_phone,  # Updated to match your column name
#             total_amount=invoice.total_amount,
#             created_at=datetime.utcnow()
#         )
#         db.add(db_invoice)
#         db.flush()

#         # Create invoice items
#         for item in invoice.items:
#             db_item = InvoiceItem(
#                 invoice_id=db_invoice.id,
#                 product_name=item.product_name,
#                 quantity=item.quantity,
#                 unit_price=item.unit_price,
#                 total_price=item.total_price
#             )
#             db.add(db_item)

#         db.commit()
#         db.refresh(db_invoice)

#         # Prepare response
#         return {
#             "id": db_invoice.id,
#             "customer_name": db_invoice.customer_name,
#             "customer_phone": db_invoice.customer_phone_invoice_number,  # Updated to match your column name
#             "total_amount": db_invoice.total_amount,
#             "created_at": db_invoice.created_at,
#             "items": [
#                 {
#                     "id": item.id,
#                     "product_name": item.product_name,
#                     "quantity": item.quantity,
#                     "unit_price": item.unit_price,
#                     "total_price": item.total_price
#                 }
#                 for item in db_invoice.items
#             ]
#         }

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.invoice.models import Invoice, InvoiceItem
from app.invoice.schemas import InvoiceCreate, Invoice as InvoiceSchema
from datetime import datetime


invoice_router = APIRouter()

@invoice_router.post("/create", status_code=201, response_model=InvoiceSchema)
# async def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
#     try:
#         # Create invoice
#         db_invoice = Invoice(
#             customer_name=invoice.customer_name,
#             customer_phone_invoice_number=invoice.customer_phone,
#             total_amount=invoice.total_amount,
#             created_at=datetime.utcnow()
#         )
#         db.add(db_invoice)
#         db.flush()

#         # Create invoice items
#         for item in invoice.items:
#             db_item = InvoiceItem(
#                 invoice_id=db_invoice.id,
#                 product_name=item.product_name,
#                 quantity=item.quantity,
#                 unit_price=item.unit_price,
#                 total_price=item.total_price
#             )
#             db.add(db_item)

#         db.commit()
#         db.refresh(db_invoice)
#         return db_invoice

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))
async def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        # Generate invoice number
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create invoice
        db_invoice = Invoice(
            customer_name=invoice.customer_name,
            customer_phone=invoice.customer_phone,  # Changed
            invoice_number=invoice_number,  # Added
            total_amount=invoice.total_amount,
            created_at=datetime.utcnow()
        )
        db.add(db_invoice)
        db.flush()

        # Create invoice items
        for item in invoice.items:
            db_item = InvoiceItem(
                invoice_id=db_invoice.id,
                product_name=item.product_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price
            )
            db.add(db_item)

        db.commit()
        db.refresh(db_invoice)
        
        return {
            "id": db_invoice.id,
            "customer_name": db_invoice.customer_name,
            "customer_phone": db_invoice.customer_phone,
            "invoice_number": db_invoice.invoice_number,
            "total_amount": db_invoice.total_amount,
            "created_at": db_invoice.created_at,
            "items": [
                {
                    "id": item.id,
                    "invoice_id": item.invoice_id,
                    "product_name": item.product_name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price
                }
                for item in db_invoice.items
            ]
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))