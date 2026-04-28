"""
Task 2 — Pydantic Models
All tool inputs/outputs are strictly typed. No raw dicts returned.
Failures return: success=False, error="message"
"""
from pydantic import BaseModel, field_validator
from typing import List, Optional, Literal


class ToolResult(BaseModel):
    """Base model for all tool results."""
    success: bool
    error: Optional[str] = None


class Product(BaseModel):
    """Represents a product in the catalog."""
    sku: str
    name: str
    price: float
    description: str


class SearchResult(ToolResult):
    """Result of a product search."""
    products: List[Product] = []


class OrderItem(BaseModel):
    """A single line item in an order."""
    sku: str
    quantity: int
    price: float


class Order(ToolResult):
    """Full order details."""
    order_id: str = ""
    customer_id: str = ""
    items: List[OrderItem] = []
    total_amount: float = 0.0
    status: str = ""


class InventoryStatus(ToolResult):
    """Inventory check result for a SKU."""
    sku: str = ""
    quantity_on_hand: int = 0
    reorder_point: int = 0
    status: str = "ok"  # ok | low | out


class Ticket(ToolResult):
    """Support ticket details."""
    ticket_id: str = ""
    customer_id: str = ""
    issue: str = ""
    priority: str = ""
    status: str = "open"

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        """Bonus A: Priority validator with Pydantic."""
        allowed = {"low", "medium", "high"}
        if v and v.lower() not in allowed:
            raise ValueError(f"Priority must be one of {allowed}, got '{v}'")
        return v.lower() if v else v
