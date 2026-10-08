# AI Learning Research — Loops Learning Module v0.4

## Status
Current Loops content-pilot learning specification.

Runtime version: `v0.4.0`.

Historical v0.2.0 and v0.3.0 remain resolvable for frozen learners.

## Learning objective
Understand and independently apply:

`INITIALIZE → ITERATE → CHECK → UPDATE → RESULT`

with a basic Python `for` loop over a list.

## Prerequisites
Variables/assignment, simple lists, comparisons, `if`, indentation, and basic Python syntax.

## Lesson 1 — How a `for` loop actually runs
The learner is taught that Python visits list values one at a time.

Example pattern:
```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

Teaching emphasis:
- the loop variable holds the current value;
- the body runs once per value;
- Python automatically advances;
- the loop stops after the final item.

A dry-run table shows iteration, list position, current value, executed code, and output.

## Lesson 2 — Conditions inside a loop
Example pattern:
```python
for number in numbers:
    if number > 20:
        print(number)
```

Execution model:

current value → evaluate condition → run/skip `if` block → next value → stop when exhausted

The lesson traces both True and False cases and reviews comparison operators.

## Lesson 3 — Building a result

### Counting
The learner is taught why counting begins at:
```python
result = 0
```

and why each qualifying item uses:
```python
result += 1
```

`result += 1` is explained as `result = result + 1`.

### Summation
The learner then sees:
```python
result += value
```

Key distinction:

| Counting | Summation |
|---|---|
| `result += 1` | `result += value` |
| add one because one item matched | add the matching value itself |

## Practice
Guided practice uses a fill-in-the-blank conditional-counting example.

Mini-practice asks the learner to predict outputs from a short conditional loop without running it.

These are instructional/familiarization activities, not primary outcomes.

## Static hints
Hints emphasize:
- identify the current value;
- check the condition;
- for counting add one;
- for summation add the matching value.

## Experimental control
Both conditions receive identical v0.4.0 material. The only treatment difference during Supported is controlled-AI availability.

## Construct boundary
Do not teach or require:
`while`, nested loops, `break`, `continue`, functions, recursion, dictionaries, comprehensions, advanced libraries, or filtered-list construction/`append` as a required target skill.

## Assessment boundary
Instructional worked examples may show complete code because both groups receive them identically.

Independent assessments must not reveal correctness, expected answers, hidden cases, or AI assistance.

## Associated current versions
- protocol v0.4
- learning module v0.4.0
- task instrument 0.3.1
- system prompt 0.3.0
- grader 0.1.0
