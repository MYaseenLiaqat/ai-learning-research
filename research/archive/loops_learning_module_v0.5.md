# AI Learning Research - Loops Learning Module v0.5

## Status

Current Loops feasibility/content-pilot learning specification.

Runtime version: `v0.5.0`.

Historical module versions remain resolvable for frozen learners.

## Learning objective

Understand and independently apply:

`INITIALIZE -> ITERATE -> CHECK -> UPDATE -> RESULT`

using a basic Python `for` loop over a provided sequence.

## Scope boundary

Teach only:

- variables
- assignment
- comparisons
- `if` statements
- `for` loops
- counters
- accumulators
- simple arithmetic
- `result`

Do not teach or require `while`, nested loops, `break`, `continue`, functions, recursion, dictionaries, comprehensions, advanced libraries, or solution shortcuts outside this scope.

## Lesson 1 - Iterator and execution order

A `for` loop takes the next value from the sequence, stores it in the iterator variable, and runs the indented body. When the body finishes, Python takes the next value and repeats the process. The iterator variable therefore represents the current value for one iteration only; it is replaced by the next value on the next iteration. After the final value, the loop ends automatically and execution continues after the loop.

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

A dry run should identify the iteration number, sequence position, current iterator value, the statement evaluated, and its effect:

| iteration | position | current `number` | body action | output |
| --------- | -------- | ---------------- | ----------- | ------ |
| 1         | 0        | 10               | print 10    | 10     |
| 2         | 1        | 20               | print 20    | 20     |
| 3         | 2        | 30               | print 30    | 30     |

The loop variable is not a counter. It holds the current item supplied by the sequence.

## Lesson 2 - Conditions and tracing

For each value, trace this order:

`get current value -> evaluate comparison -> enter or skip the if block -> update state if needed -> move to next value`

```python
numbers = [10, 25, 15]

for number in numbers:
    if number > 20:
        print(number)
```

The dry-run table records both True and False cases:

| iteration | current value | comparison         | block   | result/output |
| --------- | ------------- | ------------------ | ------- | ------------- |
| 1         | 10            | `10 > 20` is False | skipped | none          |
| 2         | 25            | `25 > 20` is True  | runs    | 25            |
| 3         | 15            | `15 > 20` is False | skipped | none          |

Use `>`, `>=`, `<`, and `<=` exactly as the task wording requires. Indentation determines which statements belong to the loop and which belong to the condition.

## Lesson 3 - State: counters and accumulators

Before the loop, decide what `result` represents and initialize it. Keep one running state across iterations.

### Counter

Use a counter when the result represents **how many** values meet a condition. Start at zero because no values have been counted before the first iteration. When a value qualifies, add one:

```python
result = 0
for value in numbers:
    if value > 20:
        result += 1
```

`result += 1` means `result = result + 1`. It counts qualifying items, regardless of the size of the current item.

| current value | qualifies? | counter before | update | counter after |
| ------------- | ---------- | -------------: | ------ | ------------: |
| start         | -          |              0 | none   |             0 |
| 10            | no         |              0 | none   |             0 |
| 25            | yes        |              0 | add 1  |             1 |
| 40            | yes        |              1 | add 1  |             2 |
| 15            | no         |              2 | none   |             2 |

### Accumulator

Use an accumulator when the result represents a total or sum. Start at zero because zero is the additive identity. When a value qualifies, add the current value, not one:

```python
result = 0
for price in prices:
    if price > 1000:
        result += price
```

`result += price` means `result = result + price`.

| current price | qualifies? | total before | update   | total after |
| ------------- | ---------- | -----------: | -------- | ----------: |
| start         | -          |            0 | none     |           0 |
| 500           | no         |            0 | none     |           0 |
| 1200          | yes        |            0 | add 1200 |        1200 |
| 800           | no         |         1200 | none     |        1200 |
| 1500          | yes        |         1200 | add 1500 |        2700 |

### Choosing the state

Ask: does `result` represent a number of matching items, or the total of their values? Choose a counter for the first question and an accumulator for the second. In every case, trace the current value, condition, state before the update, and state after the update.

## Practice

Use fill-in-the-blank counting practice and short dry-run tables. These are instructional familiarization activities, not primary outcomes. Examples may show complete code to both conditions identically; independent assessment prompts do not show expected answers or hidden tests.

## Associated versions

- research design: `v0.3`
- protocol: `v0.4`
- task instrument: `0.4.0`
- system prompt: `0.4.0`
- grader: `0.1.0`
