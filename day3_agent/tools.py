from typing import Dict, Any, List

def search_products(query: str) -> List[Dict[str, Any]]:
    """Mock tool to search for products."""
    print(f"DEBUG: Tool 'search_products' called with query='{query}'")
    return [
        {"id": "PROD-001", "name": "Laptop Pro", "sku": "SKU-123", "price": 1200},
        {"id": "PROD-002", "name": "Wireless Mouse", "sku": "SKU-456", "price": 25},
    ]

def check_inventory(sku: str) -> Dict[str, Any]:
    """Mock tool to check inventory status."""
    print(f"DEBUG: Tool 'check_inventory' called with sku='{sku}'")
    # Simulate a "low stock" scenario as per requirements
    if sku == "SKU-123":
        return {"sku": sku, "status": "low", "quantity": 2}
    return {"sku": sku, "status": "in_stock", "quantity": 50}

def create_support_ticket(title: str, priority: str = "medium") -> Dict[str, Any]:
    """Mock tool to create a support ticket."""
    print(f"DEBUG: Tool 'create_support_ticket' called with title='{title}', priority='{priority}'")
    return {
        "ticket_id": "TKT-999",
        "title": title,
        "priority": priority,
        "status": "created"
    }

# Tool Registry
TOOL_REGISTRY = {
    "search_products": search_products,
    "check_inventory": check_inventory,
    "create_support_ticket": create_support_ticket
}
