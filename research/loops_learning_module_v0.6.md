# AI Learning Research - Loops Learning Module v0.6

## Status

Current transferable loop-problem-solving learning specification.

Runtime version: `v0.6.0`.

Historical module versions remain resolvable for frozen learners.

## Learning objective

Use a `for` loop to decompose and solve unseen problems by identifying the current item, the condition, the state variables, the update rule, and the final result.

Reasoning framework:

`UNDERSTAND -> DECOMPOSE -> INITIALIZE STATE -> ITERATE -> CHECK -> UPDATE -> RESULT`

## Scope boundary

Teach only variables, assignment, `for` loops, `if/else`, counters, accumulators, comparisons, simple lists and strings, and simple arithmetic. Do not teach or require functions, dictionaries, recursion, classes, nested loops, `while`, `break`, `continue`, comprehensions, advanced libraries, or advanced algorithms.

## Core lessons

### Iterator variables and tracing

A `for` loop assigns one sequence item at a time to an iterator variable. The iterator is the current item, not automatically a counter. Trace each iteration by recording the item, condition, state before the update, action taken, and state after the update.

### Problem decomposition

Before writing code, state:

1. What does the final result represent?
2. What value or state is needed before iteration begins?
3. What is the current item?
4. What comparison or condition decides the action?
5. Which state variables change, and how?
6. What should remain after the loop ends?

### Counter pattern

Use a counter when the answer is how many items satisfy a condition. Initialize it to `0` and add `1` for each qualifying item.

### Accumulator pattern

Use an accumulator when the answer is a total. Initialize it to `0` and add the current qualifying value or simple derived amount.

### Maximum tracking

Use a maximum-state variable when the answer is the largest value seen so far. Initialize it from an appropriate first value or a clearly defined baseline, compare each current item with the stored maximum, and update it when the current item is larger. State the empty-input behavior explicitly when the task requires it.

### Multiple state variables

Some problems require more than one state variable. For a longest-streak problem, one variable can track the current streak and another can track the longest streak seen so far. On a qualifying item, increase the current streak; otherwise reset it. After each update, compare the current streak with the best streak.

Example reasoning can use simple strings in a list, such as `"yes"` and `"no"`, without introducing new data structures.

## Unseen-problem practice

Practice should vary the context and surface details while preserving the same reasoning patterns. Learners should complete a dry-run table before coding and explain why each state variable is needed. Worked examples are instructional; independent assessment prompts do not reveal expected answers or hidden tests.

## Associated versions

- task instrument: `0.5.0`
- system prompt: `0.5.0`
- grader: `0.1.0`
