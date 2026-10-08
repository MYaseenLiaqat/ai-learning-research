# AI Learning Research — Experimental Task Bank v0.1

## Design rule

All tasks target **moderate conceptual difficulty**. The purpose is to test learning, retention, and transfer—not Python trivia or code length.

Each task must be independently graded with hidden tests.

---

# A. LOOPS / ITERATION

## Construct

Iterate through a sequence, apply a condition, and maintain an appropriate result.

### A1 — Supported

**Task**

Given a list of temperatures, count how many temperatures are above 30°C.

```python
temperatures = [28, 32, 35, 29, 31, 27]
```

Expected result: `3`

**Constructs:** iteration + conditional selection + counting.

**AI:** available only in AI condition.

### A2 — Immediate Independent

**Task**

Given a list of exam scores, count how many scores are greater than or equal to 50.

```python
scores = [42, 67, 81, 39, 55, 48, 72]
```

Expected result: `4`

AI unavailable.

### A3 — Delayed Retention

**Task**

Given product prices, calculate the total price of products costing more than 1000.

```python
prices = [450, 1200, 850, 1700, 999, 1500]
```

Expected result: `4400`

AI unavailable.

### A4 — Transfer

**Task**

Given a list of temperatures, create a new list containing only temperatures above 30°C.

```python
temperatures = [25, 34, 29, 41, 31]
```

Expected result: `[34, 41, 31]`

The participant must independently construct an output rather than merely count/sum.

AI unavailable.

### A5 — Criterion

**Task**

A transaction system stores transaction amounts. Calculate the total value of transactions greater than 1000. If no transaction qualifies, the result must be 0.

The task should be presented without telling the participant which programming construct to use.

AI unavailable.

## Loop task variants

Create at least 3 equivalent variants per stage using contexts such as:

- temperatures
- exam scores
- product prices
- delivery counts
- transaction amounts
- attendance

Do not change the underlying construct or reasoning burden.

---

# B. FUNCTIONS / ABSTRACTION

## Construct

Define and call a reusable function that accepts parameters and returns a computed result.

The construct should emphasize **return values and parameterized abstraction**, not merely function syntax.

### B1 — Supported

Write a function:

`calculate_average(numbers)`

that returns the average of the numbers in a list.

Include a clear requirement for the empty-list behavior in the final version.

### B2 — Immediate Independent

Write a function:

`calculate_maximum(numbers)`

that returns the largest value in a list.

AI unavailable.

### B3 — Delayed Retention

Write a function that returns the average of only the positive measurements in a list.

The final protocol must specify the behavior when there are no positive values.

AI unavailable.

### B4 — Transfer

Write a reusable function that receives a list of measurements and a threshold, then returns how many measurements meet or exceed that threshold.

This changes the context and introduces a parameter representing a decision boundary.

AI unavailable.

### B5 — Criterion

Write a small program using at least two reusable functions to process a dataset and return a summary.

The exact criterion task should be finalized after pilot testing to ensure it remains a function-abstraction task rather than a general algorithm test.

AI unavailable.

---

# C. DICTIONARIES / KEY-VALUE REPRESENTATION

## Construct

Use a dictionary to retrieve, update, and reason about values associated with keys.

Avoid making the tasks primarily loop tasks.

### C1 — Supported

Given:

```python
scores = {
    "Ali": 82,
    "Sara": 91,
    "Hamza": 76
}
```

Write code that retrieves Sara's score.

Then modify the task slightly so the learner must update a named student's score.

The final supported episode should teach the representation and operations rather than reward memorization.

### C2 — Immediate Independent

Given a dictionary of product prices, retrieve the price associated with a specified product key and store/update it as required by the prompt.

AI unavailable.

### C3 — Delayed Retention

Given a dictionary mapping employee names to hours worked, retrieve the value for a specified employee and apply a simple rule to the result.

AI unavailable.

### C4 — Transfer

Given a dictionary mapping device IDs to status values, update the status for one specified device and then retrieve the updated value.

The context changes while the underlying key-value representation remains.

AI unavailable.

### C5 — Criterion

Given a small dictionary representing records, perform a novel key-based lookup/update task with an explicitly defined missing-key behavior.

AI unavailable.

---

# 4. Task-design constraints

For every final task:

1. No hidden prerequisite beyond the declared prerequisite set.
2. No requirement to use a specific algorithm unless the construct itself is being measured.
3. No dependence on external libraries.
4. Deterministic grading.
5. Hidden tests must include normal cases and edge cases.
6. Input sizes should remain small enough that algorithmic efficiency is not the construct.
7. Task wording must not reveal the solution pattern unnecessarily.
8. Equivalent variants must be reviewed for difficulty before participant use.

# 5. Important revision before pilot

The dictionary tasks need a more rigorous task-equivalence review than the loop tasks because dictionary operations can become either trivial lookup exercises or accidentally turn into loop problems.

The final dictionary episode should therefore be reviewed against the construct definition before protocol lock.

# 6. Scoring recommendation

Use a 0–100 task score derived from predefined behavioral components, for example:

- core behavior: 60%
- boundary/edge cases: 20%
- required input/output behavior: 20%

Do not award points for stylistic code quality in the primary outcome.

The exact weighting must be finalized before data collection.
