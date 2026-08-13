# AI Learning Research — Loops Learning Module v0.2

## Status

Current Loops pilot specification. Supersedes v0.1 for the Loops pilot. v0.1 is retained for reference and is not overwritten.

## 1. Experimental comparison

Both conditions receive the same:

- concept explanation
- worked example
- guided practice
- static hints
- supported programming task
- programming environment
- time allowance
- grading

The only treatment difference is:

- `NO_AI`: no generative-AI assistance
- `AI`: controlled generative-AI assistance during the `SUPPORTED` phase only

AI must be disabled server-side for all independent assessments.

## 2. Learning objective

After the learning episode, the participant should be able to:

> Iterate through a sequence, evaluate each element against a condition, and maintain or construct an appropriate result without relying on a memorized solution.

The first pilot focuses on basic `for`-loop iteration.

Do not introduce as new concepts:

- `while`
- nested loops
- `break`
- `continue`
- list comprehensions
- recursion
- dictionaries
- advanced libraries

## 3. Prerequisites

Participants should already understand:

- variables
- assignment
- basic numeric/string values
- comparison operators
- `if`
- basic lists
- basic Python syntax

A prerequisite/eligibility check may be used before the module. It is not a primary outcome.

## 4. Standardized explanation

A loop repeats an operation for each item in a sequence.

Example:

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

The loop takes each value from `numbers` one at a time and executes the indented block.

### Conditional iteration

```python
numbers = [10, 25, 40, 15]

for number in numbers:
    if number > 20:
        print(number)
```

The reasoning pattern is:

1. inspect each item;
2. test the condition;
3. perform the required action when the condition is true.

### Counting

```python
numbers = [10, 25, 40, 15]

count = 0

for number in numbers:
    if number > 20:
        count += 1
```

After the loop, `count == 2`.

## 5. Worked example

Problem:

> Count how many values are strictly greater than 20.

Input:

```python
numbers = [10, 25, 40, 15]
```

Reasoning:

- initialize a counter;
- inspect each value;
- test whether it is greater than 20;
- increment the counter for qualifying values.

Reference solution shown to both groups:

```python
result = 0

for number in numbers:
    if number > 20:
        result += 1
```

Expected result:

`2`

The worked example may show the complete solution because both groups receive it as instruction.

## 6. Guided practice

Problem:

> Given `stock_levels = [3, 8, 2, 6, 1]`, count how many stock levels are strictly less than 5.

Expected result:

`3`

This is practice/familiarization and is not a primary outcome.

## 7. Static hints

Both groups can access these fixed hints:

### Hint 1

Think about what value should keep track of the result while the loop runs.

### Hint 2

For each item, check whether it satisfies the required condition.

### Hint 3

When the condition is true, update the result.

The `AI` condition receives these same hints plus controlled AI access.

## 8. Supported task

> A weather station recorded:
>
> `temperatures = [28, 32, 35, 29, 31, 27]`
>
> Write a Python program that counts how many temperatures are strictly greater than 30.

The participant environment provides the input variable `temperatures`. The participant's code must assign the answer to a `result` variable.

Expected result:

`3`

Stage:

`SUPPORTED`

### Pilot controls

Working values:

- maximum supported-session duration: 20 minutes
- maximum AI requests for `AI` condition: 8

These values are pilot parameters, not final scientific constants.

## 9. AI treatment

AI is available only when:

- participant condition is `AI` / `controlled_ai`
- current stage is `SUPPORTED`
- the Supported session has been explicitly started
- the Supported session has not expired
- supported attempt is not completed
- request limit has not been exceeded

AI may:

- explain concepts
- give hints
- inspect/debug code
- suggest corrections
- show example code
- provide a complete solution if requested

The AI must not:

- reveal research hypotheses
- reveal hidden tests
- personalize the experimental treatment
- retain cross-task memory
- use RAG or external study-specific retrieval

All interactions must be logged.

## 10. Immediate Independent assessment

AI is unavailable.

> Given:
>
> `scores = [42, 67, 81, 39, 55, 48, 72]`
>
> Write a Python program that counts how many scores are greater than or equal to 50.

The participant environment provides the input variable `scores`. The participant's code must assign the answer to a `result` variable.

Expected result:

`4`

Purpose:

Immediate unaided reconstruction of conditional iteration with changed context and threshold boundary.

Immediate becomes available only after the Supported phase is completed or has expired.

## 11. Delayed retention assessment

Target pilot timing:

approximately +7 days.

AI is unavailable.

> Given:
>
> `prices = [450, 1200, 850, 1700, 999, 1500]`
>
> Write a Python program that returns the total price of products costing strictly more than 1000.

The participant environment provides the input variable `prices`. The participant's code must assign the answer to a `result` variable.

Expected result:

`4400`

Purpose:

Retention of iterative selection while changing the accumulator from count to sum.

## 12. Transfer assessment

Current backend timing is approximately +14 days. This timing remains provisional.

AI is unavailable.

> Given:
>
> `temperatures = [25, 34, 29, 41, 31]`
>
> Create a new list containing only the temperatures strictly greater than 30. Preserve the original order.

The participant environment provides the input variable `temperatures`. The participant's code must assign the answer to a `result` variable.

Expected result:

`[34, 41, 31]`

Purpose:

Transfer from scalar aggregation to constructing a filtered output.

## 13. Criterion assessment

Target pilot timing:

approximately +21 days.

AI is unavailable.

Working construct:

> Given a list of transaction amounts, return the total value of transactions strictly greater than 1000. If no transaction qualifies, return 0.

The participant environment provides the input variable `transactions`. The participant's code must assign the answer to a `result` variable.

The final seeded version must use values/context not previously shown to the participant.

Do not tell the learner which programming construct to use in the Criterion prompt.

Purpose:

Longer-term independent application without explicitly telling the learner to use a loop.

## 14. Hidden-test requirements

### Immediate

Include:

- empty list
- all below threshold
- all at/above threshold
- exact boundary value
- duplicates
- mixed values

### Delayed

Include:

- empty list
- no qualifying values
- one qualifying value
- all qualifying values
- boundary value 1000
- duplicates

### Transfer

Include:

- no qualifying values
- all qualifying values
- duplicates
- order preservation

### Criterion

Include:

- empty list
- no qualifying values
- one qualifying value
- all qualifying values
- boundary values

Hidden tests must never be returned to participants.

## 15. Grading contract

Loops tasks use a **provided-input + `result` variable** contract. The participant must NOT:

- define a function;
- understand parameters;
- understand return values;
- call a function.

For every hidden test, the grader:

1. uses a fresh execution namespace;
2. injects that test's input variables;
3. executes the participant's code;
4. retrieves the configured `result` variable;
5. compares it with the expected value;
6. records pass/fail.

A fresh namespace is required for every hidden test so state cannot leak between cases.

## 16. Scoring

Primary score should measure behavioral correctness.

For the technical pilot, use equal-weight hidden-test scoring. Research-facing conversion is `score × 100`.

This does not yet implement the proposed 60/20/20 weighting (core / edge / I/O contract). Do not award primary-outcome points for comments, formatting, variable naming style, preferred algorithm, or code length.

## 17. Required research logging

For the pilot, preserve enough information to reconstruct:

participant → condition → module version → task version → stage → timing → AI exposure → submission → score → grader version

At minimum log:

- participant ID
- condition
- task/stage
- module/task version where available
- scheduled/start/completion timestamps where available
- AI prompt/response/sequence
- submission timestamp
- score
- grader metadata/version where available

## 18. Pilot calibration questions

The 8–10 participant pilot should evaluate:

1. Is the material understandable without researcher intervention?
2. Is the supported task moderately difficult?
3. Is the 20-minute limit reasonable?
4. Is the 8-request AI budget reasonable?
5. Does the No-AI group have adequate learning support?
6. Are Immediate/Delayed/Transfer tasks too easy or too hard?
7. Do hidden tests grade intended behavior correctly?
8. Are there ceiling/floor effects?
9. Is AI usage natural or overwhelmingly solution-copying?
10. Is follow-up completion feasible?

Pilot data is for feasibility and calibration, not confirmatory causal claims.

## 19. Implementation boundary

For the next backend phase, implement only what is required to support this Loops pilot.

Do not add frontend redesign, RAG, vector databases, personalization, adaptive learning, dashboards, recommendation systems, or complex microservices.
