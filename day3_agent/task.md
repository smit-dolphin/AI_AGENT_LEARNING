# 🧠 Day 3 — Performative Task: Planning Agent (Track B)

## 🎯 Objective

Build a **Planning Agent** that clearly separates:

* **Planner → decides WHAT to do**
* **Executor → performs the actions**

You must prove this rule:

> The Planner NEVER calls tools
> The Executor NEVER decides the plan

---

## 🧩 Task Breakdown

### 🔹 Task 1 — Understand Planning

Before writing anything, answer these:

* Does the planner call tools? → ❌ No
* Where do parameters (like SKU) come from? → From the plan itself
* Should execution continue if step 1 fails? → ❌ No (dependent steps)

👉 Write these answers as comments in your code (important for understanding)

---

### 🔹 Task 2 — Build the Planner

#### 🎯 Goal:

Generate a **3-step plan** from a user request.

#### 📌 Requirements:

* Input: User request (text)
* Output: List of steps (structured plan)
* Each step must contain:

  * `step` (order number)
  * `action` (human-readable)
  * `tool` (tool name)
  * `params` (input for tool)

#### 🧠 What You Are Proving:

* Planning happens **before execution**
* No tool is called here
* Only thinking + structuring

---

### 🔹 Task 3 — Build the Executor

#### 🎯 Goal:

Execute the plan **step-by-step in order**

#### 📌 Requirements:

* Read the plan list
* Execute each step sequentially (1 → 2 → 3)
* Call tools using a registry
* Store results for later steps

#### 🧠 What You Are Proving:

* Execution is **deterministic**
* No decision-making happens here
* Executor only follows instructions

---

### 🔹 Task 4 — Connect Planner + Executor

#### 🎯 Goal:

Run the full system

#### 📌 Flow:

1. User gives request
2. Planner generates full plan
3. Plan is printed (before execution)
4. Executor runs the plan

---

## ⚙️ Execution Flow (What Actually Happens)

### Step 1 — Planner Runs

* Receives request:

  > Search product → check stock → create ticket

* Generates full plan:

  * Step 1 → search product
  * Step 2 → check inventory
  * Step 3 → create support ticket

✅ At this stage:

* NO tools are called
* Only plan is created

---

### Step 2 — Plan is Displayed

You must see ALL steps before execution begins.

👉 This proves:

* Planning is separate
* System is predictable

---

### Step 3 — Executor Starts

Now execution begins:

#### ▶ Step 1:

* Tool: search_products
* Output: Product list

#### ▶ Step 2:

* Tool: check_inventory
* Input: SKU from plan
* Output: stock status

#### ▶ Step 3:

* Tool: create_support_ticket
* Runs only if needed

---

### Step 4 — Completion

* All steps executed
* Results stored
* Final output printed

---

## 📊 Expected Behavior

You should observe:

1. Planner runs first
2. Full plan is printed
3. THEN execution starts
4. Steps run in strict order
5. All steps complete successfully

---

## 🔍 Observations You Must Check

### After Planning

* Plan is a list (not text)
* Contains exactly 3 steps
* Each step has correct structure

---

### After Execution

#### Step 1:

* Product data returned

#### Step 2:

* Correct SKU used
* Status = "low"

#### Step 3:

* Ticket created
* Priority = "high"

---

## ❌ Common Mistakes

* Planner calling tools ❌
* Executor modifying plan ❌
* Steps running out of order ❌
* Wrong tool names ❌
* JSON parsing errors ❌

---

## 🏁 Completion Criteria

You are done when:

* Planner returns structured plan
* Plan is printed BEFORE execution
* Executor runs steps sequentially
* All tools execute correctly
* You can clearly explain:

👉 Why planning and execution must be separated

---

## ⭐ Extension Task (Important)

Add a **Human Approval Step**

Before execution:

* Ask user:

  > "Does this plan look correct? Type yes to proceed"

* If NOT "yes":

  * Stop execution

---

## 🧠 Final Understanding

This task teaches:

* Deterministic AI systems
* Agent architecture basics
* Why separating thinking & acting prevents errors

---

## 💡 Real-World Insight

This pattern is used in:

* AI agents (AutoGPT-style systems)
* Workflow automation
* Safe AI systems (human approval layers)

---

🚀 After completing this, you can confidently explain:

* How planning agents work
* Why separation improves reliability
* How tools are orchestrated step-by-step

---
