# Controlled AI Tutor Policy v0.2

## Status
**Historical reconstruction.**

Reconstructed on 2026-09-08 from system prompt version `0.2.0`.

## Associated system prompt
`0.2.0`

## Purpose
Provide standardized controlled AI assistance during Supported Loops practice while constraining help to the approved construct.

## Allowed assistance
The tutor could explain concepts, give hints, discuss permitted Loops constructs, and provide a complete solution if explicitly requested, provided it stayed inside the permitted construct boundary.

## Permitted constructs
Variables, assignment, comparisons, `if`, `for`, counters/accumulators, and `result`.

## Forbidden solution constructs
List comprehensions, `while`, nested loops, `break`, `continue`, functions as the solution abstraction, recursion, dictionaries, advanced libraries, and shortcuts bypassing the target `for` loop.

## Research-integrity restrictions
The tutor was instructed not to reveal hidden tests or research hypotheses, invent tasks, personalize treatment, or use cross-task memory.

## Input contract
For the active task, the tutor used platform-provided inputs rather than redefining them. Small illustrative examples could use different inputs.

## Limitation
This version still allowed the complete active-task solution when requested. Protocol v0.4 later replaced this behavior with the constrained v0.3 tutor policy.
