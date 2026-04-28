"""
Task 8 — Tool Registry
Central lookup: agent calls TOOL_REGISTRY[tool_name](**params)
Missing tool → agent gets a clean error string, no crash.
"""
from .search_products import search_products
from .get_order_details import get_order_details
from .check_inventory import check_inventory
from .create_ticket import create_support_ticket

TOOL_REGISTRY = {
    "search_products":     search_products,
    "get_order_details":   get_order_details,
    "check_inventory":     check_inventory,
    "create_support_ticket": create_support_ticket,
}
