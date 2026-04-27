# DWS Day 1 Practical - tasks.md

## 1) Problem Statement

Build a Python ReAct agent (Claude API) that documents a PHP controller file automatically:

- Read PHP file from disk
- Find functions missing docblocks
- Generate one correct docblock per undocumented function
- Write updated PHP back to disk
- Stop when task is complete

---

## 2) Project Structure

Create this structure:

```text
day1_agent/
|-- agent.py
|-- tools.py
|-- sample_controller.php
`-- .env
```

`.env`:

```env
ANTHROPIC_API_KEY=your_real_key_here
```

Install dependencies:

```bash
pip install anthropic python-dotenv
```

---

## 3) Tools (tools.py)

Implement exactly four tools:

1. `read_file(path) -> str`
   - Reads full PHP file content.
   - Returns useful error text if read fails.

2. `find_undocumented(code) -> list[str]`
   - Finds PHP functions missing a proper docblock immediately above.
   - Returns only undocumented function names.

3. `generate_docblock(function_source) -> str`
   - Input: one function source only.
   - Output: docblock text only.
   - Must include:
     - starts with `/**`
     - description line
     - `@param` for each parameter
     - `@return`

4. `write_file(path, code) -> bool`
   - Writes updated code to disk.
   - Returns `True` on success, else `False`.

---

## 4) Sample PHP File (sample_controller.php)

Use this exact file:

```php
<?php

class ProductController {

    /**
     * Get all active products from the catalog.
     *
     * @return array
     */
    public function getActiveProducts() {
        return Product::where('status', 'active')->get();
    }

    public function getProductById($id) {
        return Product::find($id);
    }

    public function updateStock($sku, $quantity) {
        $product = Product::where('sku', $sku)->first();
        $product->stock = $quantity;
        $product->save();
        return $product;
    }

    public function createSupportTicket($customerId, $issue) {
        return SupportTicket::create([
            'customer_id' => $customerId,
            'issue'       => $issue,
            'status'      => 'open',
        ]);
    }

}
```

Expected undocumented functions:

- `getProductById`
- `updateStock`
- `createSupportTicket`

Existing docblock to preserve unchanged:

- `getActiveProducts`

---

## 5) Agent Loop (agent.py)

Load `.env`, initialize Anthropic client, set:

```python
MAX_ITERATIONS = 20
PHP_FILE_PATH = "sample_controller.php"
```

Loop follows ReAct:

- Think: what is known, what next action is needed
- Act: call one tool with exact input
- Observe: read tool result and update state

Required tool order/behavior:

1. `read_file`
2. `find_undocumented`
3. `generate_docblock` once per undocumented function (not batched)
4. insert each generated docblock in code
5. `write_file` after all needed docblocks are ready
6. stop with `end_turn` when complete

Stop conditions:

- task complete (`find_undocumented` empty)
- model returns `end_turn`
- max iterations reached (20)

---

## 6) Observe Checkpoint (after every tool call)

After `read_file`:

- Correct file loaded?
- Full source present?
- Four functions visible?

After `find_undocumented`:

- Exactly 3 missing functions?
- Correct names?
- `getActiveProducts` absent?

After each `generate_docblock`:

- Starts with `/**`
- Description matches function intent
- `@param` count/type aligns with parameters
- `@return` present
- Not copied blindly from another function

After `write_file`:

- Return value is `True`
- Re-open file and verify all inserted docblocks are present and correctly placed

---

## 7) Reasoning Checkpoints

Before writing `tools.py`, think about:

- Error behavior for missing files
- Exact regex/pattern logic for undocumented detection
- How partial/non-docblock comments are handled
- Write failure return handling

Before writing `agent.py`, think about:

- How completion is detected deterministically
- What to do if no undocumented functions on first scan
- Why docblocks must be generated one function at a time
- Where tool outputs are appended back into messages

---

## 8) Common Mistakes to Avoid

- Not appending tool results to message history
- Generating docblocks for all functions in one call
- Removing/ignoring `MAX_ITERATIONS`
- Returning wrong list from `find_undocumented`
- Writing file before all docblocks are prepared
- Skipping Observe validation

---

## 9) Expected Output

- Terminal prints each tool call and result in order
- Typical completion in ~6-10 iterations
- Final PHP file has docblocks on all 4 functions
- Original `getActiveProducts` docblock unchanged
- Every generated docblock includes description, `@param`, `@return`
- Final stop reason is `end_turn`

---

## 10) Completion Criteria

Practical is complete only when all are true:

1. Agent loop runs start-to-finish without error
2. All tool calls/results are visible in terminal output
3. All four functions are documented in file
4. Existing `getActiveProducts` docblock is unchanged word-for-word
5. New docblocks each include description, `@param`, and `@return`
6. Agent ends with `end_turn` (not max-iteration cutoff)
7. You can explain what happened on each iteration

---

## 11) Extension Tasks (Optional)

- Self-verify after write: re-read + re-run `find_undocumented` to confirm empty
- Handle zero-undocumented file and exit cleanly
- Test behavior on malformed PHP
- Add function with partial comment and confirm detection as undocumented
