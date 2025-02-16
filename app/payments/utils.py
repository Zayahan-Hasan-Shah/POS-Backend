import hashlib
from datetime import datetime

def generate_jazzcash_payload(amount: float, order_id: str, description: str, customer_mobile: str):
    """
    Generate the payload required for JazzCash API.
    
    Args:
        amount: The payment amount.
        order_id: The unique order ID.
        description: Description of the transaction.
        customer_mobile: The mobile number of the customer making the payment.
    
    Returns:
        A dictionary containing the payload.
    """
    jazzcash_merchant_id = "your_merchant_id"  # Replace with actual Merchant ID
    jazzcash_password = "your_password"        # Replace with actual Password
    jazzcash_salt = "your_salt"                # Replace with actual Salt

    # Prepare the data for hashing
    data = f"{jazzcash_merchant_id}&{order_id}&{amount}&{description}&{customer_mobile}&{jazzcash_salt}"
    hashed_signature = hashlib.sha256(data.encode()).hexdigest()

    # Generate the payload
    return {
        "merchant_id": jazzcash_merchant_id,
        "order_id": order_id,
        "amount": amount,
        "description": description,
        "customer_mobile": customer_mobile,
        "signature": hashed_signature,
        "timestamp": datetime.utcnow().strftime("%Y%m%d%H%M%S"),
    }
