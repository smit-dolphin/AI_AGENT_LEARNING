# Task 11: Reasoning Checkpoints

**Should limit=0 be rejected?**
Yes. A limit of 0 means the user is asking for 0 results, which contradicts the action of searching. In `search_products`, returning `success=False` with an error message guides the agent to provide a valid limit > 0.

**Empty search success or failure?**
Success. An empty search result means the system successfully executed the query, but no matching products were found. It should return `success=True` with an empty `products` list. Returning `success=False` would imply the search tool itself broke.

**Why string status vs Enum?**
Using a string for `status` in the `InventoryStatus` model is simpler for the LLM to process and generate, as opposed to forcing it to understand a specific Enum structure in Python. However, for stricter type safety, Pydantic's `Literal["ok", "low", "out"]` or Python `Enum` could be used. We chose simple strings for ease of LLM generation.

**How detect duplicate tickets?**
By implementing an idempotency check in `create_support_ticket`. The tool iterates over existing `TICKETS` and checks if there is already a ticket with the same `customer_id` and `issue` that is currently in the `"open"` status. If so, it returns the existing ticket instead of creating a new one.

**What if tool missing in registry?**
The agent loop should catch the `KeyError` or explicitly check if the action is `in TOOL_REGISTRY`. Instead of crashing the python script, the loop passes back `Observation: Error - Tool '...' not found` so the LLM can recognize its mistake and try a different tool name.

**How verify agent observes typed models?**
In `agent.py`, the result of the tool (a Pydantic object) is converted using `tool_result.model_dump_json()`. The agent's prompt logs `Observation: {observation}`, confirming that the exact structure dictated by the Pydantic model is what gets fed back into the reasoning loop.
