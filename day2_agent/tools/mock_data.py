"""
Task 7 — Mock Data
Static datasets for PRODUCTS, ORDERS, INVENTORY.
No live APIs are used.
"""

PRODUCTS = [
    {
        "sku": "DWS-001",
        "name": "Standard Widget",
        "price": 19.99,
        "description": "A basic widget for everyday use.",
    },
    {
        "sku": "DWS-002",
        "name": "Magento Pro Widget",
        "price": 49.99,
        "description": "High-performance widget with Magento integration.",
    },
    {
        "sku": "DWS-003",
        "name": "Magento Lite Widget",
        "price": 29.99,
        "description": "Affordable Magento compatible widget.",
    },
    {
        "sku": "DWS-004",
        "name": "Premium Gadget",
        "price": 99.99,
        "description": "Top-of-the-line gadget with all features.",
    },
    {
        "sku": "DWS-005",
        "name": "Magento 2 widget",
        "price": 100.99,
        "description": "Top-of-the-line gadget with all features.",
    },
]

ORDERS = {
    "ORD-101": {
        "order_id": "ORD-101",
        "customer_id": "CUST-001",
        "items": [
            {"sku": "DWS-001", "quantity": 2, "price": 19.99},
            {"sku": "DWS-002", "quantity": 1, "price": 49.99},
        ],
        "total_amount": 89.97,
        "status": "shipped",
    },
    "ORD-102": {
        "order_id": "ORD-102",
        "customer_id": "CUST-002",
        "items": [
            {"sku": "DWS-004", "quantity": 1, "price": 99.99},
        ],
        "total_amount": 99.99,
        "status": "processing",
    },
}

INVENTORY = {
    "DWS-001": {"quantity_on_hand": 50, "reorder_point": 10},   # status: ok
    "DWS-002": {"quantity_on_hand": 5,  "reorder_point": 15},   # status: low
    "DWS-003": {"quantity_on_hand": 0,  "reorder_point": 5},    # status: out
    "DWS-004": {"quantity_on_hand": 100, "reorder_point": 20},  # status: ok
}

# In-memory ticket store (simulates a DB for idempotency)
TICKETS: dict = {}
