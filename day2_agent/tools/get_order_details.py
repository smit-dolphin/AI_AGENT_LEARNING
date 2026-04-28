"""
Task 4 — Tool 2: get_order_details
Looks up an order from mock ORDERS by order_id.
Rules:
 - Missing order returns success=False, never raises exceptions
"""
from .models import Order, OrderItem
from .mock_data import ORDERS


def get_order_details(order_id: str) -> Order:
    """Return full order details for the given order_id."""
    data = ORDERS.get(order_id)
    if not data:
        return Order(success=False, error=f"Order '{order_id}' not found")

    items = [OrderItem(**item) for item in data["items"]]
    return Order(
        success=True,
        order_id=data["order_id"],
        customer_id=data["customer_id"],
        items=items,
        total_amount=data["total_amount"],
        status=data["status"],
    )
