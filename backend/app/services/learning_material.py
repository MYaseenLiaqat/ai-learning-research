"""Static, versioned Loops learning material for the pilot.

This revision keeps the construct narrow: basic conditional iteration with a
for-loop. Old v0.2.0 material remains available for frozen participants.
"""

LEGACY_LOOPS_MODULE_V020 = {
    "module_id": "loops",
    "version": "v0.2.0",
    "explanation": (
        "A loop repeats an operation for each item in a sequence.\n\n"
        "Example:\n"
        "    numbers = [10, 20, 30]\n"
        "    for number in numbers:\n"
        "        print(number)\n\n"
        "The loop takes each value from `numbers` one at a time and executes "
        "the indented block.\n\n"
        "### Conditional iteration\n"
        "    numbers = [10, 25, 40, 15]\n"
        "    for number in numbers:\n"
        "        if number > 20:\n"
        "            print(number)\n\n"
        "The reasoning pattern is:\n"
        "1. inspect each item;\n"
        "2. test the condition;\n"
        "3. perform the required action when the condition is true.\n\n"
        "### Counting\n"
        "    numbers = [10, 25, 40, 15]\n"
        "    count = 0\n"
        "    for number in numbers:\n"
        "        if number > 20:\n"
        "            count += 1\n\n"
        "After the loop, `count == 2`."
    ),
    "worked_example": {
        "problem": "Count how many values are strictly greater than 20.",
        "input": "numbers = [10, 25, 40, 15]",
        "reasoning": (
            "1. initialize a counter;\n"
            "2. inspect each value;\n"
            "3. test whether it is greater than 20;\n"
            "4. increment the counter for qualifying values."
        ),
        "solution": (
            "result = 0\n"
            "for number in numbers:\n"
            "    if number > 20:\n"
            "        result += 1"
        ),
        "expected_result": "2",
    },
    "guided_practice": {
        "problem": "Given `stock_levels = [3, 8, 2, 6, 1]`, count how many stock levels are strictly less than 5.",
        "expected_result": 3,
        "note": "This is practice/familiarization and is not a primary outcome.",
    },
    "static_hints": [
        "Think about what value should keep track of the result while the loop runs.",
        "For each item, check whether it satisfies the required condition.",
        "When the condition is true, update the result.",
    ],
}

LOOPS_MODULE = {
    "module_id": "loops",
    "version": "v0.3.0",
    "explanation": (
        "Learning objective: use a basic Python `for` loop to initialize a result, "
        "iterate through a sequence one item at a time, check a condition, update the result, "
        "and read the final value after the loop ends.\n\n"
        "Prerequisite reminder: variables, lists, comparisons, `if`, and indentation. "
        "You do not need a full Python course to complete this module.\n\n"
        "A `for` loop takes one item from a sequence at a time and runs the indented loop body "
        "once for each item.\n\n"
        "Example:\n"
        "    numbers = [4, 7, 2]\n"
        "    for value in numbers:\n"
        "        print(value)\n\n"
        "The current `value` changes each time the loop runs.\n\n"
        "Trace example:\n"
        "    numbers = [4, 7, 2]\n"
        "    result = 0\n"
        "    for value in numbers:\n"
        "        if value > 3:\n"
        "            result += 1\n"
        "\n"
        "iteration | value | condition | result\n"
        "1         | 4     | True      | 1\n"
        "2         | 7     | True      | 2\n"
        "3         | 2     | False     | 2\n\n"
        "Five-step reasoning framework:\n"
        "1. INITIALIZE — create the result before the loop\n"
        "2. ITERATE — process each item one at a time\n"
        "3. CHECK — test the current item against a condition\n"
        "4. UPDATE — change the result only when the condition is true\n"
        "5. RESULT — read the final value after the loop ends\n\n"
        "### Counting\n"
        "    numbers = [10, 25, 40, 15]\n"
        "    result = 0\n"
        "    for number in numbers:\n"
        "        if number > 20:\n"
        "            result += 1\n\n"
        "Here, `result = 0` is outside the loop because we want one running total. "
        "`result += 1` happens only when the condition is true.\n\n"
        "### Summing / accumulation\n"
        "    prices = [500, 1200, 800]\n"
        "    total = 0\n"
        "    for price in prices:\n"
        "        if price > 1000:\n"
        "            total += price\n\n"
        "Counting uses `result += 1`. Summation uses `result += value`.\n\n"
        "### Comparison reminder\n"
        "- `>` means strictly greater than\n"
        "- `>=` means greater than or equal to\n"
        "- `<` means strictly less than\n"
        "- `<=` means less than or equal to\n\n"
        "Use the comparison carefully: the word 'strictly' changes the threshold.\n\n"
        "### Indentation matters\n"
        "    numbers = [8, 3, 11]\n"
        "    result = 0\n"
        "    for number in numbers:\n"
        "        if number > 5:\n"
        "            result += 1\n\n"
        "The lines inside the loop and inside the `if` statement must be indented. "
        "Otherwise Python will not run the update at the correct time.\n\n"
        "### Common mistakes\n"
        "- initialize the result inside the loop instead of before it\n"
        "- use wrong indentation\n"
        "- update the result outside the condition instead of only when the condition is true\n"
        "- use the wrong comparison operator\n"
        "- overwrite a value instead of accumulating the total\n"
        "- redefine the platform-provided input variable\n"
    ),
    "worked_example": {
        "problem": "Count how many values are strictly greater than 20.",
        "input": "numbers = [10, 25, 40, 15]",
        "reasoning": (
            "1. initialize the result before the loop;\n"
            "2. inspect each value;\n"
            "3. test whether the value is greater than 20;\n"
            "4. update the result only for qualifying values;\n"
            "5. read the final result after the loop."
        ),
        "solution": (
            "result = 0\n"
            "for number in numbers:\n"
            "    if number > 20:\n"
            "        result += 1\n"
            "print(result)"
        ),
        "expected_result": 2,
    },
    "guided_practice": {
        "problem": (
            "Fill in the missing parts of this code to count how many values in `stock_levels` are "
            "strictly less than 5.\n\n"
            "```python\n"
            "stock_levels = [3, 8, 2, 6, 1]\n"
            "result = ___\n"
            "for value in stock_levels:\n"
            "    if value ___ 5:\n"
            "        result ___ 1\n"
            "```\n\n"
            "What value should the final answer be?"
        ),
        "expected_result": 3,
        "note": "This is scaffolded guided practice to reinforce the pattern. It is not a primary outcome.",
    },
    "mini_practice": {
        "problem": "Use a short list and count how many values are less than 10.",
        "example": "observations = [12, 7, 9, 15, 4]",
        "hint": "Start with result = 0, check each value, and count the ones below 10.",
    },
    "static_hints": [
        "Start by deciding what variable will hold the result before the loop begins.",
        "For each item, check the condition and update the result only when it is true.",
        "Check the final value after the loop ends, not inside the loop body.",
    ],
}

MODULE_REGISTRY = {
    "v0.2.0": LEGACY_LOOPS_MODULE_V020,
    "v0.3.0": LOOPS_MODULE,
}


def get_learning_module(version: str):
    module = MODULE_REGISTRY.get(version)
    if module is None:
        raise KeyError(f"Unknown learning module version: {version}")
    return module