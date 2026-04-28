"""
Task 5 — Tool 3: check_inventory
Returns quantity_on_hand, reorder_point, and status for a SKU.
Status logic:
  - out  → quantity_on_hand == 0
  - low  → quantity_on_hand <= reorder_point
  - ok   → otherwise
Must be idempotent: repeated calls with same SKU return same result.
"""
from .models import InventoryStatus
from .mock_data import INVENTORY


def check_inventory(sku: str) -> InventoryStatus:
    """Check stock level and status for the given SKU."""
    item = INVENTORY.get(sku)
    if not item:
        return InventoryStatus(success=False, error=f"SKU '{sku}' not found in inventory")

    qoh = item["quantity_on_hand"]
    rp  = item["reorder_point"]

    if qoh == 0:
        status = "out"
    elif qoh <= rp:
        status = "low"
    else:
        status = "ok"

    return InventoryStatus(
        success=True,
        sku=sku,
        quantity_on_hand=qoh,
        reorder_point=rp,
        status=status,
    )
