from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.invoice.models import Invoice, InvoiceItem
from app.invoice.schemas import InvoiceRequest
from app.utils.security import get_current_user

invoice_router = APIRouter()

@invoice_router.post("/create-invoice")
def create_invoice(invoice: InvoiceRequest, db: Session = Depends(get_db)):
    # Calculate total amount
    total_amount = sum(item.quantity * item.unit_price for item in invoice.items)

    # Create invoice
    new_invoice = Invoice(
        customer_name=invoice.customer_name if invoice.customer_name else "Anonymous",
        customer_phone=invoice.customer_phone if invoice.customer_phone else "1234567890",
        total_amount=total_amount
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    # Add invoice items
    for item in invoice.items:
        new_item = InvoiceItem(
            invoice_id=new_invoice.id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            total_price=item.quantity * item.unit_price
        )
        db.add(new_item)

    db.commit()
    return {"msg": "Invoice created successfully", "invoice_id": new_invoice.id, "total_amount": total_amount}
