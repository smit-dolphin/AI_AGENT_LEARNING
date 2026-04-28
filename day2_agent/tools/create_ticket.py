"""
Task 6 — Tool 4: create_support_ticket
Creates a support ticket for a customer.
Rules:
 - Priority must be: low | medium | high  (validated by Pydantic model — Bonus A)
 - Must be idempotent: same customer_id + issue returns the same ticket_id
 - Never raises exceptions
"""
import uuid
from .models import Ticket
from .mock_data import TICKETS


def create_support_ticket(customer_id: str, issue: str, priority: str) -> Ticket:
    """Create or retrieve an existing open ticket (idempotent)."""
    # Validate priority early before Pydantic to give a clean error message
    if priority.lower() not in {"low", "medium", "high"}:
        return Ticket(
            success=False,
            error=f"Invalid priority '{priority}'. Must be low | medium | high",
        )

    # Idempotency check: same customer + same issue + still open → return existing ticket
    for t in TICKETS.values():
        if (
            t["customer_id"] == customer_id
            and t["issue"] == issue
            and t["status"] == "open"
        ):
            return Ticket(success=True, **t)

    # Create new ticket
    ticket_id = f"TIC-{uuid.uuid4().hex[:8].upper()}"
    ticket_data = {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "issue": issue,
        "priority": priority.lower(),
        "status": "open",
    }
    TICKETS[ticket_id] = ticket_data

    return Ticket(success=True, **ticket_data)
