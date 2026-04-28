"""
Task 3 — Tool 1: search_products
Searches mock PRODUCTS by query string.
Rules:
 - limit=0 is rejected (returns failure)
 - Empty result is still success=True
 - No filtering/sorting mixed in
"""
from .models import SearchResult, Product
from .mock_data import PRODUCTS


def search_products(query: str, limit: int = 10) -> SearchResult:
    """Search products by name or description keyword."""
    if limit <= 0:
        return SearchResult(success=False, error="limit must be greater than 0")

    results: list[Product] = []
    q = query.lower()

    for p in PRODUCTS:
        if q in p["name"].lower() or q in p["description"].lower():
            results.append(Product(**p))
            if len(results) >= limit:
                break

    # Empty result is success — the query ran fine, just no matches
    return SearchResult(success=True, products=results)
