from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.utils.security import get_current_user
from app.payments.utils import generate_jazzcash_payload
from datetime import datetime
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

payments_router = APIRouter()

class PaymentRequest(BaseModel):
    amount: float
    description: str
    payment_method: str
    mobile_number: str = None

@payments_router.post("/process")
def process_payment(
    payment_request: PaymentRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    try:
        logger.info(f"Received payment request: {payment_request}")
        logger.info(f"Current user: {current_user}")

        # Extract data from request
        amount = payment_request.amount
        description = payment_request.description
        payment_method = payment_request.payment_method
        mobile_number = payment_request.mobile_number

        # Validate payment method
        if payment_method not in ["jazzcash", "cash"]:
            raise HTTPException(status_code=400, detail="Invalid payment method")

        # Process JazzCash payment
        if payment_method == "jazzcash":
            if not mobile_number:
                raise HTTPException(
                    status_code=400, detail="Mobile number is required for JazzCash payments"
                )
            order_id = "ORDER" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
            # Pass mobile_number to generate_jazzcash_payload
            payload = generate_jazzcash_payload(amount, order_id, description, mobile_number)
            logger.info(f"JazzCash payload generated: {payload}")
            # Simulated JazzCash response
            response = {"status": "success", "order_id": order_id}
            if response["status"] != "success":
                logger.error(f"JazzCash payment failed: {response}")
                raise HTTPException(status_code=400, detail="Payment failed")
            return {
                "msg": "Payment successful through JazzCash",
                "order_id": order_id,
                "payment_method": "JazzCash",
            }

        # Process Cash payment
        elif payment_method == "cash":
            logger.info("Processing cash payment.")
            return {
                "msg": "Payment successful through Cash",
                "payment_method": "Cash",
            }

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
