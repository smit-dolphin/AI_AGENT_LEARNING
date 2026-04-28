# Day 2 Performative Tasks — Tool Registry for Agents

## Objective
Build a production-style tool registry with typed tools for your Day 1 agent.

---

# Task 1 — Create Project Structure

Create:

```bash
day2_agent/
├── agent.py
├── tools/
│   ├── __init__.py
│   ├── models.py
│   ├── mock_data.py
│   ├── search_products.py
│   ├── get_order_details.py
│   ├── check_inventory.py
│   ├── create_ticket.py
│   └── registry.py
└── .env
```

---

# Task 2 — Build Pydantic Models (`tools/models.py`)

Implement:

- ToolResult
- Product
- SearchResult
- OrderItem
- Order
- InventoryStatus
- Ticket

Requirements:

- Typed inputs/outputs only
- No raw dictionaries returned
- Failures return:
```python
success=False
error="message"
```

---

# Task 3 — Implement Tool 1: `search_products`

Function:

```python
search_products(query: str, limit: int = 10)
```

Must:

- Search mock PRODUCTS
- Return SearchResult
- Match “Magento” should return:
  - DWS-002
  - DWS-003

Rules:

- Search only
- No filtering/sorting logic mixed in
- Empty result behavior defined

---

# Task 4 — Implement Tool 2: `get_order_details`

Function:

```python
get_order_details(order_id: str)
```

Must:

- Return typed Order model
- Pull from mock ORDERS
- Missing order:

```python
success=False
error="Order not found"
```

Never raise exceptions.

---

# Task 5 — Implement Tool 3: `check_inventory`

Function:

```python
check_inventory(sku: str)
```

Return:

- quantity_on_hand
- reorder_point
- status:
  - ok
  - low
  - out

Must be idempotent.

---

# Task 6 — Implement Tool 4: `create_support_ticket`

Function:

```python
create_support_ticket(
 customer_id: str,
 issue: str,
 priority: str
)
```

Rules:

- Validate priority:
  - low
  - medium
  - high

Returns:

- ticket_id
- status="open"

Must be idempotent:
Duplicate submissions return same ticket_id.

---

# Task 7 — Add Mock Data (`mock_data.py`)

Use provided:

- PRODUCTS
- ORDERS
- INVENTORY

Do not use live APIs.

---

# Task 8 — Build Tool Registry (`registry.py`)

Create:

```python
TOOL_REGISTRY = {
  "search_products": search_products,
  "get_order_details": get_order_details,
  "check_inventory": check_inventory,
  "create_support_ticket": create_support_ticket,
}
```

Agent should call:

```python
TOOL_REGISTRY[tool_name](**tool_params)
```

---

# Task 9 — Run Agent Scenario

Use:

```python
task = """
Search for products containing Magento.
Check inventory status of each result.
For low or out-of-stock products,
create support ticket with high priority.
"""
```

Expected:

- 2 products found
- 2 inventory checks
- 2 support tickets created
- Agent ends with:

```python
stop_reason = end_turn
```

Target:
8–12 iterations.

---

# Task 10 — Perform Observation Checks After Every Tool

Verify:

## search_products
- Returns SearchResult
- products is List[Product]
- price is float

## get_order_details
- Missing orders return failure object
- No crashes

## check_inventory
- Valid statuses only
- Repeated calls same result

## create_support_ticket
- ticket_id exists
- status open
- success True

---

# Task 11 — Reasoning Checkpoints (Answer Before Coding)

Document answers for:

- Should limit=0 be rejected?
- Empty search success or failure?
- Why string status vs Enum?
- How detect duplicate tickets?
- What if tool missing in registry?
- How verify agent observes typed models?

Submit these with code.

---

# Task 12 — Completion Criteria

Done when all are true:

- [ ] 4 tools return Pydantic models
- [ ] No tool raises exceptions
- [ ] Registry connected to agent loop
- [ ] search → inventory → ticket flow works
- [ ] Typed results visible in terminal
- [ ] Agent exits with end_turn
- [ ] Can justify each tool’s parameters

---

# Bonus Extension Tasks

Optional:

## A.
Add priority validator with Pydantic.

## B.
Add:

```python
update_product_stock(sku, quantity)
```

## C.
Break one tool intentionally:
Return raw dict and observe agent failure.

## D.
Simulate rate limiting every third order call:

```python
error="rate_limit"
```

Observe retry behavior.

----